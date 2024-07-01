<p align="center">
<img src="img/logo.png" style="border-radius: 10%;" width = "200" />
</p>

<h1 align="center">NetBanking
</h1>

<h3 align="center">Projeto de Sistema Distribuído de Bancos Financeiros utilizando API REST</h3>

![-----------------------------------------------------](img/len.png)

<div align="justify"> 
<div id="descrição"> 
<h2> Descrição do Projeto</h2>

O Pix é um sistema de pagamento instantâneo desenvolvido pelo Banco Central do Brasil, representa uma revolução do setor financeiro ao facilitar as transações bancárias de forma rápida, segura e acessível. Em resposta à crescente adesão a essa tecnologia, este projeto propõe o desenvolvimento de um sistema semelhante, adaptado para um país sem banco central, visando incluir clientes de diversos bancos em uma solução distribuída.

O sistema será implementado por meio de um consórcio bancário, permitindo a criação e o gerenciamento de contas para depósitos e transferências de valores entre diferentes bancos. Dessa forma, o projeto se estrutura em três componentes principais, cada um com requisitos específicos:

- **Cliente Bancário:** Interface intuitiva para pessoas físicas e jurídicas, permitindo o gerenciamento de suas contas e transações de forma integrada;

- **Servidor Bancário:** Centraliza e controla as transações de forma segura, garantindo que o mesmo dinheiro não seja transferido para mais de uma conta (evitando duplo gasto);

-  **Comunicação Interbancária:** Implementação de uma API que viabilize a troca de dados e comandos entre os diferentes bancos participantes, garantindo uma comunicação eficiente e segura.


</div>
</div>

![-----------------------------------------------------](img/len.png)

<h2> Autor <br></h2>
<uL>
  <li><a href="https://github.com/TAlmeida003">Thiago Neri dos Santos Almeida</a></li>

</ul>

![-----------------------------------------------------](img/len.png)

<h1 align="center"> Sumário </h1>
<div id="sumario">
	<ul>
        <li><a href="#VisaoGeral"> Visão Geral do Sistema </a></li>
        <li><a href="#Software"> Softwares Utilizadas </a></li>
        <li><a href="#Funcionalidades"> Funcionalidades do sistema</a></li>
        <li><a href="#Ordenacao"> Ordenação Total de Multicast </a></li>
        <li><a href="#API"> API REST </a></li>
        <li><a href="#Organizacao"> Organização do Código Fonte </a></li>
        <li><a href="#Logica"> Lógica de Funcionamento do Sistema </a></li>
        <li><a href="#Testes"> Testes </a></li>
        <li><a href="#Conclusao"> Conclusão </a></li>
        <li><a href="#exe"> Execução do Projeto </a></li>
        <li><a href="#Referencias"> Referências </a></li>
	</ul>	
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify">
<div id="VisaoGeral">
<h2> Visão Geral do Sistema </h2>

O projeto desenvolvido é um sistema bancário distribuído. Nesse sentido, os bancos podem se comunicar internamente e com toda a rede por meio de um sistema ponto a ponto entre cada nó (banco). Para garantir que os nós trabalhem em **consenso**, evitando a perda e a sobreposição de dados, o que pode causar a duplicidade de dinheiro, o sistema utiliza o algoritmo de **Ordenação Total de *Multicast***. Esse algoritmo será explicado em detalhes nos próximos tópicos. A seguir, é apresentado um diagrama geral do sistema, ilustrando como os bancos se comunicam:

</div>
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify">
<div id="Software">
<h2> Softwares Utilizadas </h2>

Nesta seção, são apresentados os softwares utilizados durante o desenvolvimento do projeto.

<h3> Linguagem Python</h3>

A linguagem ***Python*** foi escolhida devido à sua facilidade de aprendizado e flexibilidade. 
Sua sintaxe limpa e legível permite a rápida prototipagem de ideias e o desenvolvimento ágil de aplicações. 
Além disso, *Python* é reconhecido pela sua vasta gama de bibliotecas e frameworks que facilitam o desenvolvimento 
em diversas áreas. É importante ressaltar que a versão utilizada foi a 3.12.2.

<h3> Biblioteca Flask</h3>

A biblioteca ***Flask*** é um módulo para construção de aplicações web em *Python*. Ela oferece flexibilidade 
para o desenvolvimento de APIs, permitindo a criação de endpoints RESTful e o gerenciamento de rotas HTTP.

<h3> Biblioteca Requests</h3>

A biblioteca ***Requests*** é uma ferramenta para fazer requisições HTTP em *Python*. Ela oferece uma 
interface que simplifica o processo de envio e recebimento de dados pela internet, tornando a 
comunicação com APIs mais eficiente.

<h3>Bibliotecas Asyncio e Aiohttp</h3>

As bibliotecas ***Asyncio*** e ***Aiohttp*** foram utilizadas para implementar funcionalidades assíncronas no projeto. O *Asyncio* permite a execução de código assíncrono, facilitando a realização de tarefas concorrentes, enquanto o *Aiohttp* é utilizado para realizar requisições HTTP de maneira assíncrona, melhorando a eficiência e o desempenho das operações de rede.

<h3> Docker</h3>

O ***Docker*** é uma plataforma de implantação e execução de aplicativos em contêineres. 
Um contêiner é uma unidade leve e portátil que inclui tudo o que um aplicativo precisa 
para ser executado de forma independente, como código, bibliotecas, dependências e configurações.
O Docker oferece uma plataforma consistente para desenvolver, testar e implantar aplicativos, 
garantindo que os ambientes de desenvolvimento e produção sejam consistentes e reproduzíveis.

<h3>IDE PyCharm</h3>

A IDE ***PyCharm*** é um ambiente de desenvolvimento integrado projetado especificamente para *Python*. O *PyCharm* oferece uma 
ampla gama de recursos para aumentar a produtividade dos desenvolvedores, incluindo realce de sintaxe avançado, 
completamento automático de código, depuração integrada e suporte para controle de versão. Além disso, o PyCharm possui
integração com o *Docker*, facilitando o desenvolvimento e a implantação de aplicativo *Python* em diversos ambientes.

<h3> Insomnia </h3>

O ***Insomnia*** é uma ferramenta usada para testar APIs e atuar como cliente REST, simplificando o desenvolvimento de APIs.
Com ele, os desenvolvedores podem criar, testar e depurar suas APIs de maneira eficiente, oferecendo suporte a 
diferentes métodos de requisição, autenticação, gerenciamento de variáveis e até mesmo a criação de fluxos de trabalho 
complexos.

</div>
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify">
<div id="Funcionalidades">
<h2> Funcionalidades do Sistema</h2>

Neste tópico, são apresentadas as funcionalidades disponíveis pelo sistema:

<h3>Criação de Usuários</h3>

Uma das funcionalidades do sistema é permitir que qualquer usuário tenha uma conta para acessar toda a rede de bancos. Ao criar uma conta de usuário em um dos bancos, é possível acessar qualquer um dos outros bancos. Para se registrar no sistema, é necessário informar o nome completo, o tipo de pessoa (física ou jurídica), o número de registro (CPF ou CNPJ), o nome de usuário e a senha de acesso. A imagem abaixo ilustra o processo de registro do usuário.

> **Observações:**
> Todos os dados pessoais são únicos; portanto, o sistema não permite novos registros se um usuário já estiver registrado com esses dados. Em caso de registros concorrentes (quando bancos tentam registrar usuários com os mesmos dados), apenas um será registrado.

<h3> Criação de Contas Bancárias</h3>

O sistema também possibilita a criação de contas bancárias para operações e movimentação de dinheiro. Um usuário pode ter várias contas bancárias, tanto em um único banco quanto nos outros bancos da rede. Para criar uma conta bancária, o usuário deve informar em qual banco será criada a conta, o tipo de conta (física, jurídica ou conjunta), e o tipo de PIX para aquela conta, que pode ser o número de registro (CPF ou CNPJ), o nome de usuário, o número da conta, ou um valor aleatório. Além disso, para criar uma conta é necessario disponibilizar um valor inicial maior ou igual a R$ 50,00. A imagem abaixo mostra o processo de registro no sistema.

> **Observações:** O número de conta criado é aleatório e individual dentro do banco. Em caso de criação concorrente (usuários pedindo para criar uma conta ao mesmo tempo), o sistema possui um gerenciamento interno em cada banco que permite que apenas um usuário crie uma conta por vez. Assim, se dois usuários tentarem criar contas ao mesmo tempo e os números de contas forem iguais, apenas uma será criada, e a outra será negada, sendo gerado um novo número de conta.

<h3>Operações Bancárias</h3>

O programa desenvolvido tem a capacidade de realizar operações bancárias por meio de pacotes (um pacote é um grupo de operações que são executadas de uma só vez), internamente e/ou externamente. Nesse sentido, são disponibilizadas três operações: depósito bancário, saque e transações via PIX. Ao criar um pacote, o usuário pode escolher quais bancos realizarão a operação, quais contas realizarão a ação e quais serão as operações realizadas.

Por exemplo, o usuário A tem uma conta no banco 1 e no banco 2 e deseja realizar o seguinte pacote: depósito de R$ 50,00 e transação via PIX de R$ 150,00 na conta do banco 1, mas também deseja sacar R$ 450,00 no banco 2. Todas essas operações podem ser realizadas em um único pacote de uma só vez. Porém, caso ocorra um erro em uma das operações, o pacote é cancelado. A imagem abaixo mostra um pacote montado.

> **Observações:** Todas as operações realizadas são enviadas para todos os bancos, permitindo que todos saibam quais operações estão ocorrendo na rede.
As operações são executadas na mesma ordem entre os nós, garantindo que transações concorrentes entre bancos sejam tratadas.
O sistema possui um gerenciamento interno onde apenas uma operação pode ser enviada por vez por cada banco, evitando concorrência interna.

<h3>Extrato Bancário</h3>
 
Por fim, o banco oferece a possibilidade de acessar os dados de cada conta, permitindo visualizar os dados do(s) responsável(is) pela conta, o saldo atual e um extrato bancário com o histórico de todas as operações realizadas na conta. A imagem abaixo ilustra essa funcionalidade.

</div>
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify">
<div id="Ordenacao">
<h2>Algoritmo de Controle de Concorrência em Sistemas Distribuídos</h2>

Em sistemas distribuídos, a ordenação total de mensagens é fundamental para garantir que todas as operações bancárias e registros de usuários sejam processados na mesma ordem em todos os nós da rede. Enquanto abordagens sem ordenação podem resultar em mensagens sendo processadas em ordens diferentes nos nós, a ordenação total assegura consistência e integridade dos dados.

<h3>Relógio Vetorial</h3>

Antes de discutir o algoritmo de controle de concorrência, é crucial entender o **relógio vetorial**. Este mecanismo de ***timestamp*** é usado para capturar a ordem causal de eventos entre diferentes processos em um sistema distribuído. Cada processo mantém um vetor de contadores, onde cada entrada representa o número de eventos observados por aquele processo. Ao enviar uma mensagem, um processo inclui uma cópia de seu vetor de relógios. Ao receber uma mensagem, um processo atualiza seu vetor combinando-o com o vetor recebido, garantindo uma visão consistente da ordem de eventos entre todos os processos.

<h3>Ordenação Total com Multicast usando Relógio Vetorial</h3>

O **algoritmo de ordenação total com *multicast*** pode ser dividido em vários passos, segue uma explicação simplificada do processo:

1.	**Envio da Mensagem:** Um nó envia uma mensagem para todos os nós da rede, anexando seu vetor de relógios atual;

2.	**Recebimento da Mensagem:** Ao receber a mensagem, cada nó a coloca em um *buffer* interno ordenado pelo relógio vetorial associado. Isso garante que todas as mensagens sejam ordenadas de acordo com o relógio vetorial;

3.	**Confirmação (ACK):** Cada nó envia um ACK para todos os outros nós indicando que recebeu a mensagem;

4.	**Verificação e Execução:**
    -	Após receber ACKs de todos os nós, o nó remetente verifica se a mensagem no topo de seu *buffer* é a próxima a ser processada;

    -	Em seguida, consulta todos os outros nós para verificar se a mensagem no topo de seus *buffers* é a mesma;

    -	Se todas as réplicas concordarem que a mensagem no topo do *buffer* é a próxima na ordem global, o nós a removem do *buffer* e a executa;

    -	Caso contrário, o nó aguarda até que todas as mensagens anteriores no *buffer* tenham sido processadas.

Este algoritmo pode introduzir latência devido ao número de mensagens necessárias para confirmação e verificação, mas garante que todas as mensagens sejam entregues e processadas na ordem correta. No contexto de sistemas distribuídos como o descrito no projeto, onde operações são agrupadas em pacotes, este método proporciona uma otimização eficiente já que todos os nós já possui a mensagem e garante a consistência e a ordem das operações em todos os nós da rede.

</div>
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify">
<div id="API">
<h2> API REST </h2>



</div>
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify">
<div id="Organizacao">
<h2> Organização do Código Fonte </h2>

</div>
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify">
<div id="Logica">
<h2> Lógica de Funcionamento do Sistema </h2>

</div>
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify">
<div id="Testes">
<h2> Testes </h2>

</div>
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify">
<div id="Conclusao">
<h2> Conclusão </h2>

</div>
</div>

![-----------------------------------------------------](img/len.png)

<div align="justify"> 
<div id="exe"> 
<h2> Execução do Projeto </h2>

Este projeto pode ser executado tanto utilizando *Docker* quanto sem ele. Siga as instruções abaixo para ambas as opções:

<h3> Sem Docker </h3>

Para executar o projeto sem *Docker*, siga estes passos:

**Passo 1: Clonar o Repositório**

Abra o terminal e execute o seguinte comando para obter o código do repositório:
    
    git clone https://github.com/TAlmeida003/Concorrencia-e-Conectividade-PBL2-Banco.git

**Passo 2: Acessar o Diretório do Projeto**

Navegue para o diretório clonado:

    cd Concorrencia-e-Conectividade-PBL2-Banco

**Passo 3: Instalar as Dependências**

Execute o seguinte comando para instalar as dependências do projeto:

    pip install Flask
    pip install requests
    
**Passo 4: Executar os Projetos**

Execute o seguinte comando para iniciar a aplicação:
    
    $env:NAME="NOME_BANCO"; $env:AGENCIA="NUM_AGENCIA"; python src/app

<h3> Docker </h3>

<h4> DockerFile </h4>

Para executar o projeto, é necessário ter o *Docker* instalado na máquina. Tendo o *Docker* instalado, basta executar os seguintes comandos:

    docker build -t app .
    docker run -p NUM_AGENCIA:NUM_AGENCIA -it -e NAME=NOME_BANCO -e AGENCIA=NUM_AGENCIA app
    docker run --network host -it -e NAME=NOME_BANCO -e AGENCIA=NUM_AGENCIA app

</div>
</div>

![-----------------------------------------------------](img/len.png)
<div align="justify">
<div id="Referencias">
<h2> Referências </h2>

</div>
</div>
