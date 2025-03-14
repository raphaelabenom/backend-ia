# API de Avaliação de Redações

## Descrição

Esta API oferece serviços para avaliação de redações e gerador de redação por tema utilizando inteligência artificial, OpenAI integrada com Langgraph. 
- Ela avalia diferentes aspectos de uma redação, como relevância, gramática, estrutura e profundidade, além de fornecer feeback para melhorar a redação em termos de organização, coesão e coerência baseada na nota obtida.
- Ela gera redação exemplo que é adequada para uso em contextos educacionais, como preparação para provas, revisão de conteúdos e inspiração para redações próprias.

A API também conta com um sistema de autenticação JWT (JSON Web Token) para garantir que apenas usuários autenticados possam utilizar seus serviços.

## Tecnologias

- **FastAPI** para criação da API.
- **Uvicorn** para execução da aplicação.
- **OpenAI** para análise de textos e geração de pontuações.
- **Langgraph** para orquestração de workflows com IA.
- **JWT** para autenticação de usuários.
- **Loguru** para logs

## Requisitos

Antes de usar a API, certifique-se de ter as seguintes dependências:

- Python 3.8 ou superior
- Bibliotecas Python:
  - FastAPI
  - Uvicorn
  - Langchain
  - Langgraph
  - OpenAI
  - PyJWT
  - dotenv
  - loguru

## Instalação

### Passo 1: Clone o repositório

Clone este repositório para o seu ambiente local:

```bash
git clone https://github.com/raphaelabenom/backend-ia.git
cd backend-ia
```

### Passo 2: Instale as dependências
Instale as dependências necessárias usando o pip:

```bash
pip install -r requirements.txt
```
### Passo 3: Configuração das variáveis de ambiente
Crie um arquivo .env na raiz do projeto com as seguintes variáveis:

```bash
OPENAI_API_KEY=<Sua_Chave_API_da_OpenAI>
```

### Passo 4: Execute a aplicação
Para executar a API localmente, use o comando:

```bash
uvicorn main:app --reload
```

Isso iniciará o servidor localmente em http://127.0.0.1:8000.

## Funcionalidades da API

### 1. Autenticação (JWT)
Antes de utilizar as rotas protegidas, você precisa autenticar-se usando um usuário e senha válidos. Após a autenticação, você receberá um token JWT, que deve ser incluído nas requisições subsequentes.

Endpoint: /token
- Método: POST
- Descrição: Recebe o nome de usuário e senha e retorna um token de acesso.
- Corpo:

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

Resposta:

```json
{
  "access_token": "<token_jwt>",
  "token_type": "bearer"
}

```

### 2. Avaliação de Redação
Este endpoint permite que você envie uma redação para ser avaliada, recebendo as pontuações baseadas em relevância, gramática, estrutura, profundidade, e a pontuação final.

Endpoint: /v1/grade_essay
- Método: POST
- Descrição: Avalia a redação enviada, retornando as pontuações em diferentes categorias.

Corpo:

```json
{
  "essay": "Texto da redação a ser avaliada"
}

```
Cabeçalho:
- Authorization: Bearer <seu_token_jwt>

Resposta:

```json
{
  "final_score": 8.5,
  "relevance_score": 7.0,
  "grammar_score": 9.0,
  "structure_score": 8.0,
  "depth_score": 8.5
  "corrections": ""
}

```

### 3. Gerador de redação

O endpoint /v1/generate_exemplary_essay gera uma redação exemplar com base em um tema fornecido. 
A redação gerada segue as diretrizes de qualidade, organização e coesão, e é adequada para uso educacional e de referência.

```json
{
  "theme": "Os impactos da tecnologia na educação"
}

```

Cabeçalho:
- Authorization: Bearer <seu_token_jwt>

Resposta:

```json
{
   "essay": "Redação exemplo"
}

```

## Swagger UI
A API é documentada automaticamente com o Swagger. Você pode acessar a documentação interativa do Swagger UI na seguinte URL após executar a aplicação:

1. Obtenção do Token
Primeiramente, você deve autenticar-se usando o endpoint /token com o nome de usuário e a senha. Isso retornará um token JWT.

```bash
POST http://127.0.0.1:8000/token

```

2. Avaliar a Redação
Agora, use o token obtido para autenticar-se e enviar uma redação para avaliação.

```bash
POST http://127.0.0.1:8000/v1/grade_essay

```
3. Gerar Redação
Se você deseja gerar uma redação a partir de um tema específicio, envie o tema da redação para o endpoint:

```bash
POST http://127.0.0.1:8000/v1/generate_exemplary_essay

```

## Exemplos de Uso

#### Redação para Teste

```json
{
  "essay": "Norberto Bobbio, cientista político italiano, afirma que a democracia é um processo que tem, em seu cerne, o objetivo de garantia a representatividade política de todas as pessoas. Para que o mecanismo democrático funcione, então, é fundamental apresentar uma rede estatal que dê acesso a diversos recursos, como alimentação, moradia, educação, segurança, saúde e participação eleitoral. Contudo, muitos brasileiros, por não terem uma certidão de nascimento, são privados desses direitos básicos e têm seus próprios papéis de cidadãos invisibilizados. Logo, deve-se discutir as raízes históricas desse problema e as suas consequências nocivas.\n\nPrimeiramente, vê-se que o apagamento social gerado pela falta de registro civil apresenta suas origens no passado. Para o sociólogo Karl Marx, as desigualdades são geradas por condições econômicas anteriores ao nascimento de cada ser, de forma que, infelizmente, nem todos recebam as mesmas oportunidades financeiras e sociais ao longo da vida. Sob esse viés, o materialismo histórico de Marx é válido para analisar o drama dos que vivem sem certificado de nascimento no Brasil, pois é provável que eles pertençam a linhagens familiares que também não tiveram acesso ao registro. Assim, a desigualdade social continua sendo perpetuada, afetando grupos que já foram profundamente atingidos pelas raízes coloniais e patriarcais da nação. Dessa forma, é essencial que o governo quebre esse ciclo que exclui, sobretudo, pobres, mulheres, indígenas e pretos.\n\nAlém disso, nota-se que esse processo injusto cria chagas profundas na democracia nacional. No livro \"Vidas Secas\", de Graciliano Ramos, é apresentada a história de uma família sertaneja que luta para sobreviver sem apoio estatal. Nesse contexto, os personagens Fabiano e Sinhá Vitória têm dois filhos que não possuem certidão de nascimento. Por conta dessa situação de registro irregular, os dois meninos sequer apresentam nomes, o que é impensável na sociedade contemporânea, uma vez que o nome de um indivíduo faz parte da construção integral da sua identidade. Ademais, as crianças retratadas na obra são semelhantes a muitas outras do Brasil que não usufruem de políticas públicas da infância e da adolescência devido à falta de documentos, o que precisa ser modificado urgentemente para que se estabeleça uma democracia realmente participativa tal qual aquela prevista por Bobbio.\n\nPortanto, o registro civil deve ser incentivado de maneira mais efetiva no país. O Estado criará um mutirão nacional intitulado \"Meu Registro, Minha Identidade\". Esse projeto funcionará por meio da união entre movimentos sociais, comunidades locais e órgãos governamentais municipais, estaduais e federais, visto que é necessária uma ação coletiva visando a consolidação da cidadania brasileira. Com o trabalho desses agentes, serão enviados profissionais a todas as cidades em busca de pessoas que, finalmente, terão suas certidões de nascimento confeccionadas, além de receberem acompanhamento e incentivo para a realização de cadastro em outros serviços importantes do sistema nacional. Por conseguinte, o Brasil estará agindo ativamente para reparar suas injustiças históricas e para solidificar sua democracia, de maneira que os seus cidadãos sejam vistos igualmente."
}
```


#### Script para requisição

```python

import requests

# URL da API
url = "URL DA API"

# Cabeçalhos da requisição
headers = {
    "accept": "application/json",
    "Authorization": "Bearer Token", # Gerando na autenticação
    "Content-Type": "application/json"
}

# Corpo da requisição (payload)
data = {
    "theme": 10
}

# Fazendo a requisição POST
response = requests.post(url, headers=headers, json=data)

# Verificando a resposta
if response.status_code == 200:
    print("Requisição bem-sucedida!")
    print("Resposta:", response.json())
else:
    print(f"Erro na requisição. Código de status: {response.status_code}")
    print("Resposta:", response.text)

```

```bash
curl -X POST "http://localhost:8000/token" 
-H "accept: application/json" 
-H "Content-Type: application/x-www-form-urlencoded" 
-d "username=testuser&password=testpassword"

curl -X POST "http://localhost:8000/v1/grade_essay" 
-H "accept: application/json" 
-H "Authorization: Bearer seu_token_aqui" 
-H "Content-Type: application/json" 
-d '{
  "essay":"Redação aqui"
  }'

curl -X POST http://localhost:8000/v1/generate_exemplary_essay \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <token>" \
-d '{
  "theme": "Os impactos da tecnologia na educação"
}'

```

### Erros Comuns
- 400: Requisição inválida (por exemplo, dados ausentes ou mal formatados)
- 401: Não autorizado (token de acesso inválido ou ausente)
- 422: Erro de validação (dados não correspondem ao modelo esperado)
- 500: Erro interno do servidor

### Logs

A API utiliza loguru para registrar informações importantes. Verifique os logs regularmente para monitorar o desempenho e identificar possíveis problemas.

Esta documentação fornece uma visão geral abrangente da API de Avaliação de Redações, cobrindo desde a instalação até o seu uso.

## Extensões Futuras
Diversificação de Temas : Expandir o serviço para suportar uma variedade maior de temas e níveis de dificuldade.
Customização : Permitir que os usuários especifiquem o número de palavras ou o nível de complexidade da redação.