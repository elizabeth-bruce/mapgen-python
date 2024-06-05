import os
import lupa.luajit20 as lupa

from fnmatch import fnmatch

TEST_DIRECTORY = './test/'
LUA_FILE_PATTERN = "*test_*.lua"

LUA_REQUIRE_LUAUNIT = """
luaunit = require('test.resources.luaunit.luaunit')
"""

LUA_RUN_TESTS = """
local runner = luaunit.LuaUnit.new()
runner:setOutputType("text")
os.exit(runner:runSuite('-v'))
"""

lua = lupa.LuaRuntime(register_eval=False, unpack_returned_tuples=False)

lua.execute(LUA_REQUIRE_LUAUNIT)
lua_filenames = []

for path, subdirs, files in os.walk(TEST_DIRECTORY):
    for name in files:
        if fnmatch(name, LUA_FILE_PATTERN):
            lua_filenames.append(os.path.join(path, name))

for lua_filename in lua_filenames:
    with open(lua_filename, 'r') as lua_file:
        lua_file_text = lua_file.read()
        lua.execute(lua_file_text)

lua.execute(LUA_RUN_TESTS)
