from spice import app

#TextHandler
import os
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter

class Handler:
  @staticmethod
  def web_path():
    return app.config['UPLOAD_WEB_PATH']

  @staticmethod
  def process(record):
    pass

  @staticmethod
  def remove(record):
    pass

  @staticmethod
  def data(record):
    return {
      "link": "%s/%s" % (Handler.web_path(), record.filename),
      "name": record.name,
      "created": record.created
    }

  @staticmethod
  def template():
    return 'default-handler.html'


class ImageHandler(Handler):

  @staticmethod
  def data(record):
    return {
      "image": "%s/%s" % (Handler.web_path(), record.filename),
      "name": record.name,
      "created": record.created
    }

  @staticmethod
  def template():
    return 'images.html'

class TextHandler(Handler):
  @staticmethod
  def data(record):
    html = ''
    print record.filetype
    if record.filetype == '.txt':
      fh = open(os.path.join(record.path, record.filename), 'r')
      html = '<pre>%s</pre>' % fh.read()
    elif record.filetype == '.md':
      pass
    else:
      fh = open(os.path.join(record.path, record.filename), 'r')
      lexer = get_lexer_for_filename(record.name)
      formatter = HtmlFormatter()
      html = highlight(fh.read(), lexer, formatter)
      fh.close()

    return {
      "link": "%s/%s" % (Handler.web_path(), record.filename),
      "name": record.name,
      "created": record.created,
      "html": html
    }

  @staticmethod
  def template():
    return 'text.html'


handlers = {
  'images': {
    'name': 'images',
    'extensions': ['.png', '.jpg', '.gif', '.bmp'],
    'class': ImageHandler
   },
  'text': {
    'name': 'text',
    'extensions': [
      #things pygments can do
      '.croc', '.dg', '.factor', '.fy', '.fancypack', '.io', '.lua', '.wlua',
      '.md', '.moon', '.pl', '.pm', '.py3tb', '.py', '.pyw', '.sc',
      'SConstruct', 'SConscript', '.tac', '.sage', '.pytb', '.rb', '.rbw',
      'Rakefile', '.rake', '.gemspec', '.rbx', '.duby', '.tcl', '.c-objdump',
      '.s', '.cpp-objdump', '.c++-objdump', '.cxx-objdump', '.d-objdump',
      '.s', '.S', '.ll', '.asm', '.ASM', '.objdump', '.adb', '.ads', '.ada',
      '.bmx', '.c', '.h', '.idc', '.cbl', '.CBL', '.cob', '.COB', '.cpy',
      '.CPY', '.cpp', '.hpp', '.c++', '.h++', '.cc', '.hh', '.cxx', '.hxx',
      '.C', '.H', '.cp', '.CPP', '.cu', '.cuh', '.pyx', '.pxd', '.pxi', '.d',
      '.di', '.pas', '.dylan-console', '.dylan', '.dyl', '.intr', '.lid',
      '.hdp', '.ec', '.eh', '.fan', '.flx', '.flxh', '.f', '.f90', '.F',
      '.F90', '.vert', '.frag', '.geo', '.go', '.x', '.xi', '.xm', '.xmi',
      '.def', '.mod', '.monkey', '.nim', '.nimrod', '.m', '.h', '.mm', '.hh',
      '.ooc', '.prolog', '.pro', '.pl', '.rs', '.rc', '.vala', '.vapi',
      '.smali', '.boo', '.aspx', '.asax', '.ascx', '.ashx', '.asmx', '.axd',
      '.cs', '.fs', '.fsi', '.n', '.aspx', '.asax', '.ascx', '.ashx', '.asmx',
      '.axd', '.vb', '.bas', '.PRG', '.prg', '.cl', '.lisp', '.el', '.v',
      '.ex', '.exs', '.erl', '.hrl', '.es', '.escript', '.erl-sh', '.hs',
      '.kk', '.kki', '.lhs', '.lsp', '.nl', '.ml', '.mli', '.mll', '.mly',
      '.opa', '.rkt', '.rktl', '.sml', '.sig', '.fun', '.scm', '.ss', '.sv',
      '.svh', '.v', '.vhdl', '.vhd', '.aj', '.ceylon', '.clj', '.gs', '.gsx',
      '.gsp', '.vark', '.gst', '.groovy', '.ik', '.java', '.kt', '.scala',
      '.xtend', '.bug', '.pro', '.jag', '.bug', '.jl', '.m', '.mu', '.m',
      '.Rout', '.Rd', '.S', '.R', '.Rhistory', '.Rprofile', '.sci', '.sce',
      '.tst', '.stan', '.abap', '.applescript', '.asy', '.au3', '.ahk',
      '.ahkl', '.awk', '.befunge', '.bf', '.b', '.bro', '.bas', '.cf', '.ecl',
      '.feature', '.plot', '.plt', '.gdc', '.hy', '.hyb', '.lgt', '.moo',
      '.maql', '.mo', '.msc', '.nsi', '.nsh', '.ns2', '.p', '.cls', '.ps',
      '.eps', '.pov', '.inc', '.proto', '.pp', '.spec', '.r', '.r3', '.cw',
      '.txt', '.robot', '.st', '.snobol', '.sp', '.u', '.rpf', '.G', '.g',
      '.rl', '.treetop', '.tt', '.sh', '.ksh', '.bash', '.ebuild', '.eclass',
      '.bashrc', 'bashrc', '.sh-session', '.bat', '.cmd',
      '.ps1', '.shell-session', '.tcsh', '.csh', '.txt', '.sql',
      '.sqlite3-console', '.tmpl', '.spt', '.cfm', '.cfml', '.cfc', '.html',
      '.evoque', '.xml', '.kid', '.phtml', '.jsp', '.mao', '.m', '.mhtml',
      '.mc', '.mi', 'autohandler', 'dhandler', '.myt', 'autodelegate',
      '.rhtml', '.tpl', '.ssp', '.tea', '.vm', '.fhtml', '.cmake',
      'CMakeLists.txt', '.dpatch', '.darcspatch', '.diff', '.patch', '.pot',
      '.po', '.man', '.hxml', '.ini', '.cfg', '.weechatlog', '.mak',
      'Makefile', 'makefile', 'Makefile.', 'GNUmakefile', '.properties',
      '.pypylog', '.reg', '.rst', '.rest', '.tex', '.aux', '.toc', '.vim',
      '.vimrc', '.exrc', '.gvimrc', 'vimrc', 'exrc', 'gvimrc', 'vimrc',
      'gvimrc', '.yaml', '.yml', '.as', '.as', '.coffee', '.css', '.dart',
      '.dtd', '.duel', '.jbst', '.haml', '.hx', '.html', '.htm', '.xhtml',
      '.xslt', '.jade', '.js', '.json', '.lasso', '.ls', '.mxml', '.j',
      '.php', '.php3', '.php4 .php5', '.inc', '.qml', '.sass', '.scaml',
      '.scss', '.ts', '.xqy', '.xquery', '.xq', '.xql', '.xqm', '.xml',
      '.xsl', '.rss', '.xslt', '.xsd', '.wsdl', '.xsl', '.xslt', '.xpl'
      #non pygment files
      , '.md'
    ],
    'class': TextHandler
   }
}


def get_handler(extension):
  global handlers
  for key in handlers.keys():
    handler = handlers[key]
    if extension in handler['extensions']:
      return handler
  return {
    "name": "default",
    "class": Handler,
  }
