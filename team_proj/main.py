import ast
import os
with open('base.py', 'r') as file:
    source = ''.join(file.readlines())
    root = ast.parse(source)

    internal_functions = []
    called_functions = []
    direct_calls = []
    indirect_calls = []

    direct_imports = []
    from_imports = []

    imported_path = set()

    # print(ast.dump(root))
    for node in ast.walk(root):
        # import @@@
        if(isinstance(node, ast.Import)):
            for node in node.names:
                direct_imports.append('/'.join(node.name.split('.')))

        # from @@@ import ###
        if(isinstance(node, ast.ImportFrom)):
            for iter in node.names:
                from_imports.append({'path': '/'.join(node.module.split('.')), 'name': iter.name})

        # function call
        # 클래스 통해서 호출하는것도 여기로 들어옴.
        if(isinstance(node, ast.Call)):
            print(ast.dump(node))
            if(isinstance(node.func, ast.Attribute)):
                indirect_calls.append({'module': node.func.value.id, 'function': node.func.attr})
            if(isinstance(node.func, ast.Name)):
                direct_calls.append(node.func.id)
        
        # function def
        if(isinstance(node, ast.FunctionDef)):
            internal_functions.append(node.name)

    # print("내부 정의한 함수들", internal_functions)
    # print('직접 호출', direct_calls)
    # print('간접 호출', indirect_calls)
    # for call in direct_calls:
    #     if(call not in internal_functions):
    #         print(f"{call} is imported from outside")

    for node in direct_imports:
        path = node + '.py'
        result = os.popen(f"find {path}").readlines()
        if(result != []):
            imported_path.add(path)
            
    for node in from_imports:
        path = node['path'] + '.py'
        result = os.popen(f"find {path}").readlines()
        # path.py를 찾을 수 있으면, name은 import한 함수나 클래스 이름이 되는거임
        # 찾을 수 없다면, name까지 붙여서 전체를 찾게되는 거임
        if(result == []):
            path = node['path'] + '/' + node['name'] + '.py'
        
        result = os.popen(f"find {path}").readlines()
        if(result != []):
            imported_path.add(path)
        
    print("임포트한 경로들", imported_path)