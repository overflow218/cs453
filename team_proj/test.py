'''
논문에 나온 기본 개념
Em -> Mutated expression
Sm -> Em을 포함하는 statement

파이썬 ast로 파싱하면 expression이랑 statement는 구분할 수 있을거같음. 
블록은 따로 안정해주고 있으니까 함수 정의나 if/for/while 등 새로운 제어문이 활용되는 경우라고 생각해야할듯.

Bm -> Sm을 포함하는 block

아마 맥락상 뮤턴트들을 싹다 만들어두고, 그런 다음에 아래의 항목들을 구해야하는것 같음
이게 구현이 어려운 이유는 AST로 코드를 파싱하면서 
1. 각 노드를 block, statement, expression의 단위로 나누고 이들의 연결 관계를 다 표시해야함
2. 그러면서 expression에서 mutation을 만들고 생성된 mutation의 개수를 세어줘야함. 
3. 1,2를 통해 생성된 feature들에 대해 선정된 뮤테이션을 다시 골라와야하는데 이게 쉽냐는거지. 
그러면 2번에서 뮤테이션을 만들지 말고 만들 수 있는 경우 카운트만 높여주는 방식을 활용해볼 수도 있겠다.

뮤테이션이 생성되는 단위는 expression 기준이라고 정해놓으면
각 statement 별로 내부에 포함된 expression을 불러올 수 있어야함. 
역시 마찬가지로 block에서도 내부에 포함된 모든 statement를 불러올 수 있어야함. 
그래서 뮤턴트의 개수를 구할때는 block -> statement -> expression 
재귀적으로 내려가는 구조가 이루어져야할듯

Complexity: Complexity of Sm , approximated by the number of mutants on Sm
-> 대략 맥락상 Sm 스테이트먼트에 있는 다른 뮤턴트들의 개수를 의미하는듯함.

control flow graph를 그려야함.
CfgDepth: Depth of Bm according to CFG.
-> 시작 블록부터 Bm 블록까지 경로의 길이
사실상 모든 블록이 뮤테이션이 있다고 말할 수 있으니깐, 이건 블록의 깊이를 구할 수 있으면 될듯. 
글고 이건 딱히 mutation testing과는 연관이 없는 feature인것 같음.

CfgPredNum: Number of predecessor basic blocks, in CFG, of Bm. 
-> Bm에 진입하는 블록들의 개수
블록이 함수인 경우에는 이 함수를 호출하는 경로가 다 포함될것이고 
if문/for문 같은 블록의 경우 해당 블록을 포함하는 상위 블록 1개가 될거임

근데 문제는 이거 찾으려면 해당 함수 정의가 있는 곳뿐만아니라 전체 코드를 다 뒤져서 찾아야하는건데
너무 빡세지 않나...

현재 생각나는 방법은 전역적으로 block, stmt, expression을 담아놓을 수 있는 dict같은걸 만들어두고 
필요한 정보가 나올때마다 이를 찾아오도록 해야하는건가? 생각해보면 컴퓨터가 하는거니까 또 금방 할 수 있을 것도 같긴한데..

CfgSuccNum: Number of successors basic blocks, in CFG, of Bm. 
-> Bm에서 나가는 블록들의 개수.... -> 이 feature가 제일 애매한거 같음. 
파이썬은 switch가 없으니까 if/for등의 블록을 생각해주면 될 것 같음. 
함수 호출이 나오는게 아니라면 이걸 포함하는 상위 블록의 흐름으로 돌아가는거니까 1개라고 생각하면 될듯?
함수호출이 나온다면 그쪽으로 넘어가는거니까 그게 하나의 블록이 될듯?

AstNumParents: Number of AST parents of Em .
-> 말그대로 AST트리에서 부모 노드의 개수. 아마 루트부터 몇번 타고 내려와야하는지를 의미하는듯함.
이것도 무슨 의미가 있지?

data dependency 그래프를 그려야함.
이거 그냥 뽑기만 하는거는 assign이랑 name 나오는걸로 구분하면 되는데 
이제 타고 타고 들어갔을때를 어떻게 구현할지가 문제임. 생각해보면 변수 정의 -> 함수인자로 사용 
저게 그냥 depedency인거고 함수 안에서 쓰는거는 함수 안에서 따로 분석해주면 될듯. 
그렇게 생각하면 하나의 파일 내에 있는 내용들에 대해서는 어찌어찌 data dependency 구할 수 있을듯.

NumOutDataDeps: Number of mutants on expressions data-dependent on Em. 
-> Em에 데이터 의존성이 있는 expression에 있는 뮤턴트의 개수

NumInDataDeps: Number of mutants on expressions that Em is data-dependent. 
-> Em이 데이터 의존성을 가지는 expression에 생성된 뮤턴트의 개수

control depedency 그래프를 그려야함.
NumOutCtrlDeps: Number of mutants on statements control-dependents on Em. 
-> Em에 컨트롤 의존성이 있는 statement에 있는 뮤턴트의 개수
NumInCtrlDeps: Number of mutants on expressions that Em is control-dependent 
-> Em이 컨트롤 의존성을 가지는 expression에 있는 뮤턴트의 개수


NumTieDeps: Number of mutants on Em.
-> Em에 있는 뮤턴트의 개수. 전체 Expression을 의미하는건가.

이걸 다 구현했따고 했을때 궁금한저음 이거 점수를 어떻게 메겨서 어떻게 쓸거임?

'''