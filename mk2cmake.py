#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import string
import random
import os
import argparse


# Makefileにインジェクトする文字列ファイルをランダムなファイル名で生成する
# classが破壊されるとともに，ファイルは削除される
class makefileInjectant:
    def __init__(self):
        #ランダム文字列の注入物質ファイル名を生成
        self.injectant = """print-%:
	@echo '$($*)'"""
        self.path_to_injectant =\
            os.getcwd() + '/.__'+''.join([random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for i in range(10)])\
             + '.mk'
        f = open(self.path_to_injectant, 'w')
        f.write(self.injectant)
        f.close()
    def getPathToInjectant(self):
        return self.path_to_injectant
    def __del__(self):
        os.remove(self.path_to_injectant)

# Makefileへのパスと変数名から，変数内容をテキストで出力 utf-8で出力
def getMakefileVariableText(path_to_makefile_, variable_):
    inj = makefileInjectant()
    path_to_injectant = inj.getPathToInjectant()
    # print(path_to_injectant)
    ord_val = 'print-' + variable_
    mkout = subprocess.check_output(['make','-C', os.path.dirname(path_to_makefile_),  '-f', path_to_injectant, '-f', path_to_makefile_, ord_val]).decode('utf8')
    return mkout

# Makefileへのパスと変数名から，変数内容を配列で出力
def getMakefileVariable(path_to_makefile_, variable_):
    val_text = getMakefileVariableText(path_to_makefile_, variable_)
    val_text_split = val_text.split(' ')
    vals = []
    for v in val_text_split:
        if((v == '') | (v == '\n')):
            continue
        vals.append(v.replace('\n', ''))
    return vals

def main():

    # 引数
    # パーサの作成
    psr = argparse.ArgumentParser()
    psr.add_argument('--path_to_makefile', '-i', \
        default='./Makefile', \
        type=str, \
        help='Path to CubeMX generated Makefile')
    psr.add_argument('--path_to_output_directory', '-o', \
        default='.', \
        type=str, \
        nargs=1, \
        help='Path to otuput directory of CMakeists.txt')

    arg = psr.parse_args()

    ############################################
    # SET DEFAULF TOOL CHAIN PATH
    ############################################
    path_to_default_toolchain = '/opt/env/gcc-arm-none-eabi-6-2017-q2-update'

    path_to_makefile = arg.path_to_makefile
    path_to_cmakelists_template = './template/CMakeLists.txt'
    path_to_output = arg.path_to_output_directory[0] + '/CMakeLists.txt'

    # print(path_to_makefile)
    # print(path_to_output)

    # path_to_makefile = './Makefile'
    # path_to_output = './CMakeLists.txt'


    # inj = makefileInjectant()

    # mkout = subprocess.check_output(['make', '-f', 'inj.mk', '-f', 'Makefile', 'print-C_SOURCES']).decode('utf8')
    # print(mkout)
    # print(mkout.replace(' ', '\n'))
    # print(mkout.split(' '))
    # print(getMakefileVariableText('Makefile', 'C_SOURCES').split(' '))
    # print(getMakefileVariable(path_to_makefile, 'OBJECTS'))

    # for i in getMakefileVariable('Makefile', 'TARGET'):
    #     print(i)

    root_dir = "${PROJECT_SOURCE_DIR}"

    # CMakeLists.txtのテンプレートを読み込み
    cmake_template_ = open(path_to_cmakelists_template).read()
    cmake_template = cmake_template_
    
    # 出力用ファイルハンドラ
    f_out = open(path_to_output, 'w')

    

    ##############################################
    # プロジェクト設定
    ##############################################
    target_name = getMakefileVariable(path_to_makefile, 'TARGET')[0]
    set_project = 'PROJECT(' + target_name + ' C CXX ASM)'

    #テンプレートを置換
    cmake_template = cmake_template.replace("###%PROJECT%###", set_project)


    ##############################################
    # ソース，インクルードディレクトリ関係の情報をあつめる
    ##############################################

    # C source の設定
    set_c_sources  = 'SET(C_SOURCES '
    c_sources = getMakefileVariable(path_to_makefile, 'C_SOURCES')
    for i in c_sources:
        set_c_sources = set_c_sources + root_dir + '/' + i + ' '
    set_c_sources = set_c_sources + ')'
    print('###########################################')
    print(set_c_sources)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%C_SOURCES%###', set_c_sources)


    # ASM source の設定
    set_asm_sources = 'SET(ASM_SOURCES '
    asm_sources = getMakefileVariable(path_to_makefile, 'ASM_SOURCES')
    for i in asm_sources:
        set_asm_sources = set_asm_sources + root_dir + '/' + i + ' '
    set_asm_sources = set_asm_sources + ')'
    print('###########################################')
    print(set_asm_sources)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%ASM_SOURCES%###', set_asm_sources)

    # C include dirs の設定
    set_c_includes = 'SET(C_INCLUDES '
    c_includes = getMakefileVariable(path_to_makefile, 'C_INCLUDES')
    for i in c_includes:
        inc_d = root_dir + '/' + i.replace('-I', '') + ' '
        set_c_includes = set_c_includes + inc_d
    set_c_includes = set_c_includes + ')'
    # include dirs 設定コマンド
    set_include_directories_c = 'INCLUDE_DIRECTORIES(${C_INCLUDES})'
    print('###########################################')
    print(set_c_includes)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%C_INCLUDES%###', set_c_includes)


    # ASM include dirs の設定
    set_as_includes = 'SET(AS_INCLUDES '
    as_includes = getMakefileVariable(path_to_makefile, 'AS_INCLUDES')
    for i in as_includes:
        inc_d = root_dir + '/' + i.replace('-I', '') + ' '
        set_as_includes = set_as_includes + inc_d
    set_as_includes = set_as_includes + ')'
    # include dirs 設定コマンド
    set_include_directories_as = 'INCLUDE_DIRECTORIES(${AS_INCLUDES})'
    print('###########################################')
    print(set_as_includes)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%ASM_INCLDUES%###', set_as_includes)


    ##############################################
    # define系の設定
    ##############################################
    as_defines = getMakefileVariable(path_to_makefile, 'AS_DEFS')
    c_defines = getMakefileVariable(path_to_makefile, 'C_DEFS')

    set_add_definitions = ''
    for i in as_defines:
        set_add_definitions = set_add_definitions + 'add_definitions(' + i + ')\n'
    for i in  c_defines:
        set_add_definitions = set_add_definitions + 'add_definitions(' + i + ')\n'
    
    print('###########################################')
    print(set_add_definitions)
    
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%DEFINITIONS%###', set_add_definitions)

    
    ##############################################
    # コンパイラのフラグ関係の情報を集める
    ##############################################

    # MCU関係
    set_mcu = 'SET(MCU "'
    mcu_options = getMakefileVariable(path_to_makefile, 'MCU')
    for i in mcu_options:
        set_mcu = set_mcu + i + ' '
    set_mcu = set_mcu + '")'
    print('###########################################')
    print(set_mcu)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%MCU%###', set_mcu)
    
    # 最適化オプション
    set_opt = 'SET(OPT "'
    opt_options = getMakefileVariable(path_to_makefile, 'OPT')
    for i in opt_options:
        set_opt = set_opt + i + ' '
    set_opt = set_opt + '")'
    print('###########################################')
    print(set_opt)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%OPT%###', set_opt)

    # アセンブラフラグ
    set_asflags = 'SET(ASFLAGS "-x assembler-with-cpp ${MCU} ${OPT} -Wall -fdata-sections -ffunction-sections")'
    set_cmake_asm_flags = 'SET(CMAKE_ASM_FLAGS ${ASFLAGS})'
    print('###########################################')
    print(set_asflags)
    print(set_cmake_asm_flags)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%ASM_FLAGS%###', set_asflags)

    # Cコンパイラフラグ
    set_cflags = 'SET(CFLAGS "${MCU} ${OPT} -Wall -fdata-sections -ffunction-sections -g -gdwarf-2")'
    set_cmake_c_flags = 'SET(CMAKE_C_FLAGS ${CFLAGS})'
    print('###########################################')
    print(set_cflags)
    print(set_cmake_c_flags)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%C_FLAGS%###', set_cflags)

    #### リンカフラグ ####
    # リンカスクリプトパス
    set_ldscript = 'SET(LDSCRIPT '
    ldscripts = getMakefileVariable(path_to_makefile, 'LDSCRIPT')
    for i in ldscripts:
        p2ldscript = root_dir + '/' + i + ' '
        set_ldscript = set_ldscript + p2ldscript
    set_ldscript = set_ldscript + ')'
    print('###########################################')
    print(set_ldscript)    
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%LDSCRIPTS%###', set_ldscript)

    # ライブラリ
    set_libs = 'SET(LIBS "'
    libs = getMakefileVariable(path_to_makefile, 'LIBS')
    for i in libs:
        set_libs = set_libs + i + ' '
    set_libs = set_libs + '")'
    print('###########################################')
    print(set_libs)    
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%LIBS%###', set_libs)

    # リンカフラグ
    set_ldflags = 'SET(LDFLAGS "${MCU} -specs=nano.specs -T${LDSCRIPT} ${LIBS} -Wl,-Map=${PROJECT_BINARY_DIR}/${PROJECT_NAME}.map,--cref -Wl,--gc-sections")'
    print('###########################################')
    print(set_ldflags)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%LDFLAGS%###', set_ldflags)

    # リンカフラグ設定
    set_cmake_exe_linker_flags = 'SET(CMAKE_EXE_LINKER_FLAGS ${LDFLAGS})'

    ##############################################
    # クロスコンパイラのパス
    ##############################################
    path_to_bin_dirs  = getMakefileVariable(path_to_makefile, 'BINPATH')
    path_to_bin_dir = ''
    path_to_bin_dir_cxx = ''
    if(len(path_to_bin_dirs) == 0) :
        path_to_bin_dir = path_to_default_toolchain + "/bin"
        path_to_bin_dir_cxx = path_to_bin_dir
    else :
        path_to_bin_dir = ''
        path_to_bin_dir_cxx = path_to_bin_dirs[0]

    bin_prefix = getMakefileVariable(path_to_makefile, 'PREFIX')[0]
    path_to_cc = path_to_bin_dir + getMakefileVariable(path_to_makefile, 'CC')[0]
    path_to_cxx = path_to_bin_dir_cxx + '/' + bin_prefix + 'g++'
    path_to_as = path_to_cc
    path_to_cp = path_to_bin_dir + getMakefileVariable(path_to_makefile, 'CP')[0]
    path_to_ar = path_to_bin_dir + getMakefileVariable(path_to_makefile, 'AR')[0]
    path_to_sz = path_to_bin_dir + getMakefileVariable(path_to_makefile, 'SZ')[0]
    print('###########################################')
    print(path_to_bin_dir)
    print(bin_prefix)
    print(path_to_cc)
    print(path_to_cxx)
    print(path_to_as)
    print(path_to_cp)
    print(path_to_ar)
    print(path_to_sz)

    set_cmake_c_compiler = 'SET(CMAKE_C_COMPILER ' + path_to_cc + ')'
    set_cmake_cxx_compiler = 'SET(CMAKE_CXX_COMPILER ' + path_to_cxx + ')'
    set_cmake_asm_compiler = 'SET(CMAKE_ASM_COMPILER ' + path_to_as + ')'
    set_cp = 'SET(OBJCP ' + path_to_cp + ')'
    print('###########################################')
    print(set_cmake_asm_compiler)
    print(set_cmake_c_compiler)
    print(set_cmake_cxx_compiler)
    print(set_cp)

    #テンプレートを置換
    cmake_template = cmake_template.replace('###%C_COMPILER%###', set_cmake_c_compiler)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%CXX_COMPILER%###', set_cmake_cxx_compiler)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%ASM_COMPILER%###', set_cmake_asm_compiler)
    #テンプレートを置換
    cmake_template = cmake_template.replace('###%CP%###', set_cp)

    

    ##############################################
    # 置換テンプレートを保存
    ##############################################
    print('############################################')
    print(cmake_template)
    f_out.write(cmake_template)
    f_out.close()



if __name__ == '__main__': main()








