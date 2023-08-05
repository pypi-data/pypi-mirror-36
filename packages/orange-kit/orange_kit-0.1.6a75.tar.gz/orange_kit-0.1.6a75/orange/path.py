# 项目：standard python lib
# 模块：path and file
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-11 12:21
# 修改：2016-04-13 21:01
# 修改：2016-08-13 新增__iter__ 和 extractall功能
# 修订：2016-11-19
# 修订：2018-05-25 增加write_tables功能
# 修订：2018-09-12 为 Path 增加 verinfo 功能

import pathlib
import os
from codecs import BOM_UTF8, BOM_LE, BOM_BE
from orange.click import command, arg

BOM_CODE = {
    BOM_UTF8: 'utf_8',
    BOM_LE: 'utf_16_le',
    BOM_BE: 'utf_16_be',
}

DEFAULT_CODES = 'utf8', 'gbk', 'utf16', 'big5'

NT = os.name == 'nt'
POSIX = os.name == 'posix'


def is_installed(file_name: str)->bool:
    '''
    确认指定的文件是否已被安装。
    '''
    from sysconfig import get_path
    paths = [get_path(name) for name in ('platlib', 'scripts')]
    if os.name == 'nt':
        file_name = file_name.lower()
        paths = [path.lower() for path in paths]
    return any([file_name.startswith(path) for path in paths])


def is_dev(cmd: str = None)->bool:
    import sys
    cmd = cmd or sys.argv[0]
    if('wsgi' in cmd):
        return False
    return 'test' in cmd or (not is_installed(cmd))


def decode(d: bytes)->str:
    '''
    对指定的二进制，进行智能解码，适配适当的编码。按行返回字符串。
    '''
    for k in BOM_CODE:
        if k == d[:len(k)]:
            return d[len(k):].decode(BOM_CODE[k])
    for encoding in DEFAULT_CODES:
        try:
            return d.decode(encoding)
        except:
            pass
    raise Exception('解码失败')


_Parent = pathlib.WindowsPath if os.name == 'nt' else pathlib.PosixPath


class Path(_Parent):
    __slots__ = ()

    def __bool__(self):
        '''判断文件是否存在'''
        return self.exists()

    def __new__(cls, path='.', *args, **kwargs):
        if isinstance(path, str):
            if path.startswith('~'):  # 支持用户目录开头
                path = os.path.expanduser(path)
            elif path[0] in('%', '$'):  # 支持环境变量转义
                path = os.path.expandvars(path)
        return super().__new__(cls, path, *args, **kwargs)

    def read(self, *args, **kwargs):
        '''以指定的参数读取文件'''
        with self.open(*args, **kwargs)as fn:
            return fn.read()

    def ensure(self, parents=True):
        '''确保目录存在，如果目录不存在则直接创建'''
        if not self.exists():
            self.mkdir(parents=parents)

    @property
    def text(self):
        '''读取文件，并返回字符串'''
        return decode(self.read('rb'))

    @text.setter
    def text(self, text):
        '''写入文本文件'''
        self.write(text=text)

    @property
    def lines(self):
        '''按行读取文件'''
        return self.text.splitlines()

    @lines.setter
    def lines(self, lines):
        '''按行写入文件'''
        self.write(*lines)

    def write(self, *lines, text=None, data=None, encoding='utf8',
              parents=False):
        '''写文件'''
        if parents:
            self.parent.ensure()
        if lines:
            text = "\n".join(lines)
        if text:
            data = text.encode(encoding)
        if data:
            with self.open('wb')as fn:
                fn.write(data)

    def sheets(self, index=None):
        ''' 提供读取指定worksheet的功能，其中index可以为序号，
            也可以为表的名称。'''
        import xlrd
        book = xlrd.open_workbook(filename=str(self))
        if isinstance(index, int):
            sheet = book.sheet_by_index(index)
        elif isinstance(index, str):
            sheet = book.sheet_by_name(index)
        return sheet and sheet._cell_values

    def iter_sheets(self):
        '''如果指定的文件为excel文件，则可以迭代读取本文件的数据。
        返回：表的索引、表名、数据'''
        import xlrd
        book = xlrd.open_workbook(filename=str(self))
        for index, sheet in enumerate(book.sheets()):
            yield index, sheet.name, sheet._cell_values

    def iter_csv(self, encoding=None, errors=None, dialect='excel', **kw):
        import csv

        def reader():
            with open(str(self), encoding=encoding, errors=errors) as f:
                yield from f

        return csv.reader(reader(), dialect=dialect, **kw)

    @property
    def xmlroot(self):
        '''如果指定的文件为xml文件，则返回本文件的根元素'''
        from lxml.etree import parse
        return parse(str(self)).getroot()

    def __iter__(self):
        '''根据文件的不同，迭代返回不同的内容。支持如下文件：
        1、文本文件，按行返回文本
        2、Excel文件，返回表索引、表名及表中数据
        3、目录，则返回本目录下所有文件
        4、del文件，按行返回数据。
        5、csv文件，按行返回数据。
        '''
        if self.is_dir():
            return self.glob('*')
        suffix = self.lsuffix
        if suffix.startswith('.xls'):
            return self.iter_sheets()
        elif suffix == '.xml':
            return self.xmlroot.iterchildren()
        elif suffix == '.del':
            import re
            none_pattern = re.compile(",(?=,)")
            for line in self.lines:
                if line:
                    yield eval(none_pattern.sub(",None", line))
        elif suffix == '.csv':
            import csv
            with self.open() as fn:
                yield from csv.reader(fn)

    def extractall(self, path='.', members=None):
        '''如本文件为tar打包文件，则解压缩至指定目录'''
        import tarfile
        path = str(Path(path))
        tarfile.open(str(self), 'r').extractall(path, members)

    @property
    def lsuffix(self):
        '''返回小写的扩展名'''
        return self.suffix.lower()

    @property
    def pname(self):
        '''返回不带扩展名的文件名'''
        return self.with_suffix("").name

    def rmtree(self):
        '''删除整个目录'''
        import shutil
        shutil.rmtree(str(self))

    def chdir(self):
        if self.is_dir():
            os.chdir(str(self))

    def write_xlsx(self, *args, force=False, formats=None, writer=None, **kw):
        if self and not force:
            s = input('%s 已存在，请确认是否覆盖，Y or N?\n' % self.name)
            if s.upper() != 'Y':
                return
        from .xlsx import Book
        if callable(writer):
            with Book(str(self), formats=formats)as book:
                writer(book, *args, **kw)
        else:
            return Book(str(self), formats=formats, **kw)

    @property
    def mtime(self):
        '''文件修改时间'''
        return int(self.lstat().st_mtime)

    @property
    def ctime(self):
        '''文件创建时间'''
        return int(self.lstat().st_ctime)

    @property
    def uri(self):
        '''统一网址'''
        ur = self.resolve().as_uri()
        return ur.lower() if NT else ur

    @property
    def fullname(self):
        path = str(self.absolute())
        return path.lower() if NT else path

    @property
    def verinfo(self):
        name = self.name
        TYPES = {
            '.tar.gz': 'Source',
            '.tar': 'Source',
            '.whl': 'Wheel'
        }
        lname = name.lower()
        for suffix, type_ in TYPES.items():
            if lname.endswith(suffix):
                name = name[:-len(suffix)]
                break
        if type_ == 'Source':
            d = name.split('-')
            version = d[-1]
            name = '-'.join(d[:-1])
            return name, version
        elif type_ == 'Wheel':
            d = name.split('-')
            attrs = dict(zip(('version', 'abi', 'platform'), d[-3:]))
            version = d[-4]
            name = '-'.join(d[:-4])
            return name, version, attrs

    @property
    def atime(self):
        '''文件访问时间'''
        return int(self.lstat().st_atime)

    def write_tables(self, *tables,  **kw):
        '''
        写入多张表格，支持以下参数：
        formats:预设格式
        tables:为列表，每个table为字典，参数值如下：
        pos:位置
        columns:表格格式
        data:数据
        sheet:表格名称
        '''
        def writer(book, *tables):
            for table in tables:
                pos = table.pop('pos', 'A1')
                book.add_table(pos, **table)

        self.write_xlsx(writer=writer, *tables, **kw)


@command(description='Windows 格式文件转换为 Unix 文件格式')
@arg('files', nargs='*', help='待转换的文件', metavar='file')
def convert(files):
    for file in files:
        Path(file).lines = Path(file).lines
        print('转换文件"%s"成功' % (file))


if __name__ == '__main__':
    root = Path('~/Onedrive/pylib')
    for path in root.glob('*.*'):
        print(*path.verinfo, sep='\t')
