import marshal
import os
import shutil
from copy import deepcopy as dcopy
from functools import wraps
from random import choices
from string import ascii_letters, digits
from time import time_ns
from types import FunctionType as FuncType
from typing import Callable, Iterable

from geflex_db import _new_ast
from .utils import File, ObjectWrapperDecorated, DecoratedMeta
from .path import Path
from .tables import *

__all__ = 'FileColumnsEditor', 'TableFile'


class FileInnerObject(metaclass=ObjectWrapperDecorated):
    __slots__ = 'obj', 'parent'
    class_changers = {dict: ('clear', 'pop', 'popitem', 'setdefault',
                             'update'),
                      list: ('append', 'clear', 'extend', 'insert', 'pop',
                             'remove', 'reverse', 'sort'),
                      set: ('add', 'clear', 'difference_update', 'discard',
                            'intersection_update', 'pop', 'remove',
                            'symmetric_difference_update', 'update'),
                      InnerObject: ('__setitem__',)}

    def __key__(self):
        return self.obj

    @staticmethod
    @DecoratedMeta.decorate('__setitem__')
    def _changer(func: Callable):
        @wraps(func)
        def wrapper(self, *args, __object__=None, **kwargs):
            if __object__ is None:
                __object__ = self
            parent_changer = self.parent._changer(func)
            return parent_changer(self.parent, *args, __object__=__object__, **kwargs)
        return wrapper

    def __init__(self, obj, parent):
        self.parent = parent
        self.obj = obj

    def __getitem__(self, item):
        return self.__class__(self.obj[item], self)

    def __getattr__(self, method_name):
        if hasattr(self.obj.__class__, method_name):
            method = getattr(self.obj.__class__, method_name)
        else:
            method = getattr(self.obj, method_name)

        def wrap(*args, **kwargs):
            return self.parent._changer(method)(self.parent, *args, __object__=self.obj, **kwargs)

        if self.obj.__class__ in self.class_changers:
            if method_name not in self.class_changers[self.obj.__class__]:
                return method
        return wrap

    def __setattr__(self, key, value):
        if key in self.__slots__:
            super().__setattr__(key, value)
        else:
            self.parent._changer(self.obj.__class__.__setattr__)(self.parent, key, value, __object__=self.obj)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.obj}, {self.parent})'


class FileColumnsEditor(ColumnsEditor, metaclass=DecoratedMeta):
    changers = ('rename',
                'set',
                'add',
                'append',
                'insert',
                '__setitem__',
                '__iadd__',
                '__iand__',
                '__isub__',)

    @staticmethod
    @DecoratedMeta.decorate(changers)
    def _changer(func: Callable):
        @wraps(func)
        def wrap(self, *args, **kwargs):
            # noinspection PyCallingNonCallable
            result = func(self, *args, **kwargs)

            self._parent.changes_counter += 1
            if self._parent.save_interval and self._parent.changes_counter:
                if self._parent.changes_counter % self._parent.save_interval == 0:
                    self._parent.save()
            return result

        return wrap


class TableFile(Table, File):
    DATA_FILENAME = 'data'
    CACHE_PATH = 'cache'
    FILES_PATH = 'files'
    COPIES_PATH = 'copies'
    EXTENSION = 'grms'
    READABLE_ARGS = ('_columns', '_keys', '_funcs', 'name', '_paths_for_copies', '_items')

    changers = ('update',
                'diff_upd',
                'intersection_upd',
                'sort',
                'filter',
                'insert',
                'clear',
                '_normalise',
                '__setitem__',
                '__delitem__')

    @staticmethod
    @DecoratedMeta.decorate(changers)
    def _changer(func: Callable):
        """При вызове декорированного им метода, увеличивает значение счетчика изменений на 1"""
        @wraps(func)
        def wrap(self: 'TableFile', *args, __object__=None, **kwargs):
            if __object__ is None:
                __object__ = self
            result = func(__object__, *args, **kwargs)

            self.changes_counter += 1
            if self.save_interval and self.changes_counter:
                if self.changes_counter % self.save_interval == 0:
                    self.save()
            return result

        return wrap

    @staticmethod
    @DecoratedMeta.decorate('loads',)
    def _saving_off(func: Callable):
        """Отключает счетчик изменений во время выполнения функции"""
        @wraps(func)
        def wrap(self: 'TableFile', *args, **kwargs):
            save_interval = self.save_interval
            changes_counter = self.changes_counter
            self.save_interval = 0

            try:
                result = func(self, *args, **kwargs)
            finally:
                self.save_interval = save_interval
                self.changes_counter = changes_counter

            self.save_interval = save_interval
            self.changes_counter = changes_counter + 1
            if self.save_interval and self.changes_counter:
                if self.changes_counter % self.save_interval == 0:
                    self.save()
            return result

        return wrap

    @staticmethod
    @DecoratedMeta.decorate('clear',)
    def _save_copies(func: Callable):
        """Создает копии таблицы перед вызовом декорируемой функции"""
        @wraps(func)
        def wrap(self: 'TableFile', *args, **kwargs):
            self.save_copies()
            func(self, *args, **kwargs)

        return wrap

    def _reopen(self, read=False):
        path_to_file = self._path.get_child(f'\\{TableFile.DATA_FILENAME}.{TableFile.EXTENSION}').abs_path
        try:
            self.file.close()
        except (NameError, AttributeError):
            pass
        if os.path.exists(path_to_file):
            self.file = open(path_to_file, 'r+', encoding='utf-8')
            if read:
                self.changes_counter -= 1
                self.read()
        else:
            open(path_to_file, 'w').close()
            self.file = open(path_to_file, 'r+', encoding='utf-8')
            self.saves_counter -= 1
            sync_interval = self.sync_interval
            self.sync_interval = 0
            self.save()
            self.sync_interval = sync_interval

    def _mkdirs(self):
        self._path_for_files = self._path.get_child(TableFile.FILES_PATH)
        self._cache_path = self._path.get_child(TableFile.CACHE_PATH)
        self._paths_for_copies = [self._path.get_child(p.path) for p in self._paths_for_copies]
        self.parent_cache = self._cache_path
        self.cache = []

        for path in [self._path, self._path_for_files] + self._paths_for_copies:
            if not os.path.exists(path.abs_path):
                os.mkdir(path.abs_path)

    @staticmethod
    def _parse_str(data: str) -> dict:
        if data and bytes(data[0], encoding='utf-8') == b'\xef\xbb\xbf':
            data = data[1:]
        attrs, last_list_arg = {}, []
        _new_ast.SAFE_DATATYPES.append(Path)

        for line in data.splitlines():
            if line.startswith(' '):
                attrs[last_list_arg].append(_new_ast.literal_eval(line.lstrip()))
            else:
                arg, val = line.split('=', 1)
                arg, val = arg.strip(), val.lstrip()
                if val is '':
                    attrs[arg] = []
                    last_list_arg = arg
                else:
                    attrs[arg] = _new_ast.literal_eval(val)
                    last_list_arg = []  # unhashable type

        _new_ast.SAFE_DATATYPES.remove(Path)
        return attrs

    @staticmethod
    def _finalize_parsing(attrs: dict, check_items=False) -> dict:
        # noinspection PyArgumentList
        attrs['_funcs'] = [FuncType(marshal.loads(code), globals(), name) for code, name in attrs['_funcs']]
        if check_items:
            assert not any((not isinstance(l, list) for l in attrs['_items']))
        return attrs

    @property
    def columns(self):
        return FileColumnsEditor(self)

    @columns.setter
    def columns(self, value):
        FileColumnsEditor(self).set(lst=value)

    @property
    def path(self):
        return self._path.path

    @path.setter
    def path(self, value):
        self._path = Path(value)
        self._mkdirs()
        self._reopen(read=False)
        self.save()

    @property
    def path_for_copies(self):
        return [p.path for p in self._paths_for_copies]

    @path_for_copies.setter
    def path_for_copies(self, value):
        for p in value:
            if p not in self._paths_for_copies:
                self._paths_for_copies.append(self._path.get_child(p))
        if self._path.get_child(TableFile.COPIES_PATH) not in self._paths_for_copies:
            self._paths_for_copies.append(self._path.get_child(TableFile.COPIES_PATH))

    @property
    def path_for_files(self):
        return self._path_for_files

    @property
    def cache_path(self):
        return self._cache_path

    def __init__(self, path: str,
                 columns: Iterable[str],
                 keys: Iterable[str] = None,
                 funcs: Iterable[Callable] = None,
                 name='no_name',
                 paths_for_copies: Iterable[str] = None,
                 save_interval=0,
                 sync_interval=0,
                 read=False):
        super().__init__(columns, keys, funcs, name)
        super(File).__init__()

        assert type(save_interval) is int if save_interval is not None else True
        assert type(sync_interval) is int if sync_interval is not None else True

        self._path = Path(path)
        if not paths_for_copies:
            paths_for_copies = [TableFile.COPIES_PATH]
        else:
            paths_for_copies = list(paths_for_copies)

        self._paths_for_copies = [self._path.get_child(p) for p in paths_for_copies]

        self.changes_counter = 0
        self.saves_counter = 0
        self.save_interval = save_interval
        self.sync_interval = sync_interval

        self._mkdirs()
        self._reopen(read=read)

    @classmethod
    def open(cls, path, save_interval=0, sync_interval=0):
        """Инициализирует таблицу из файла"""
        with open(path + f'\\{cls.DATA_FILENAME}.{cls.EXTENSION}', 'r', encoding='utf-8') as file:
            attrs = cls._parse_str(file.read())
        attrs = cls._finalize_parsing(attrs, check_items=False)
        new_table = cls(path=path,
                        columns=attrs['_columns'],
                        keys=attrs['_keys'],
                        funcs=attrs['_funcs'],
                        name=attrs['name'],
                        paths_for_copies=[p.abs_path for p in attrs['_paths_for_copies']],
                        save_interval=save_interval,
                        sync_interval=sync_interval,
                        read=False)
        new_table._items = attrs['_items']
        return new_table

    def __del__(self):
        def remove(parent_cache):
            # 0 - cache, 1 - parent_cache
            if isinstance(parent_cache, Path):
                shutil.rmtree(parent_cache.abs_path, ignore_errors=True)
            elif not parent_cache[0]:
                remove(parent_cache[1])

        try:
            self.file.close()
        except (NameError, AttributeError):
            pass

        if not isinstance(self.parent_cache, Path):
            self.parent_cache[0].remove(self._path.abs_path)

        if not self.cache:
            remove(self.parent_cache)

        if os.path.exists(self._path.abs_path):
            if not os.listdir(self._path.abs_path):
                shutil.rmtree(self._path.abs_path, ignore_errors=True)

    def delete_file(self):
        """Удаляет директорию таблицы"""
        path = self._path.abs_path
        self.file.close()
        shutil.rmtree(path, ignore_errors=True)

    def read(self, path=None):
        """Считывает таблицу из файла"""
        if path is None:
            self.loads(self.file.read())
        else:
            with open(path, 'r', encoding='utf-8') as file:
                self.loads(file.read())

    def loads(self, data: str=None):
        """Считывает таблицу из строки, сгенерированной функцией 'dumps'"""
        data = self._parse_str(data)
        data = self._finalize_parsing(data, check_items=False)
        for attr, value in data.items():
            if attr in TableFile.READABLE_ARGS:
                setattr(self, attr, value)
            else:
                raise ValueError(f'No attribute with name {attr}')

    def save(self, path=None):
        """Сохраняет таблицу в файл"""
        if path is None:
            self.file.seek(0)
            self.file.truncate()
            self.file.write(self.dumps())
            self.file.read()
        else:
            with open(path, 'w', encoding='utf-8') as file:
                file.write(self.dumps())

        self.saves_counter += 1
        if self.sync_interval and self.saves_counter % self.sync_interval == 0:
            self.save_copies()

    def dumps(self, obj=None):
        """Возвращает строковое представление объекта для записи в файд"""
        if obj is None:
            obj = self
        # noinspection PyUnresolvedReferences
        data = f'name = {repr(obj.name)}\n' \
               f'_paths_for_copies = {obj._paths_for_copies}\n' \
               f'_columns = {obj._columns}\n' \
               f'_keys = {obj._keys}\n' \
               f'_funcs = {[(marshal.dumps(func.__code__), func.__name__) for func in obj._funcs]}\n' \
               f'_items = \n'
        return data + '\n'.join([str(l) for l in obj._items])

    def save_copies(self):
        """Сохраняет копии данных таблицы в директориях self.paths_for_copies"""
        filename = f'\\{self.name} - {time_ns()}.{TableFile.EXTENSION}'
        str_for_file = self.dumps()
        for path_for_copy in self._paths_for_copies:
            file = open(path_for_copy.abs_path + filename, 'w', encoding='utf-8')
            file.write(str_for_file)
            file.close()

    def clone(self, path=None, copyitems=False, copy_counters=False):
        """
        Создает копию таблицы
        :param path:
        :param copyitems:
        :param copy_counters:
        :return:
        """
        if path is None:
            path = self._cache_path.abs_path
        if not os.path.exists(path):
            os.mkdir(path)

        rand = ''.join(choices(ascii_letters + digits, k=4))
        new = self.__class__(
            columns=dcopy(self._columns),
            keys=dcopy(self._keys),
            funcs=dcopy(self._funcs),
            name=dcopy(self.name),
            path=f'{self.cache_path}\\{self.name} {time_ns()}{rand}',
            paths_for_copies=[p.path for p in self._paths_for_copies],
            save_interval=dcopy(self.save_interval),
            sync_interval=dcopy(self.sync_interval),
            read=False,
        )
        self.cache.append(new._path.abs_path)
        new.parent_cache = (self.cache, self.parent_cache)
        if copyitems:
            new._items = dcopy(self._items)
        if copy_counters:
            new.changes_counter = self.changes_counter
            new.saves_counter = self.saves_counter
        return new

    # ------------------------------------------------------------------------
    #   Funcs, which returns saveable objects
    # ------------------------------------------------------------------------

    def _iterator(self, iterator, saving):
        for item in iterator:
            if saving:
                yield FileInnerObject(item, self)
            else:
                yield item

    def lists(self, saving=True):
        return self._iterator(super().lists(), saving)

    def positions(self, saving=True):
        return self._iterator(super().positions(), saving)

    def _get(self, item, saving):
        if saving:
            return FileInnerObject(item, self)
        return item

    def get(self, index, saving=True):
        return self._get(super().get(index), saving)

    def get_pos(self, index, saving=True):
        return self._get(super().get_pos(index), saving)
