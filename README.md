# A3-de-Sistemas-Distribuidos
Um trabalho da UNIFACS
UC Sistemas Distribuidos

<h1> <b>Projeto A3</b> </h1>

<h2> <b>Descrição</b> </h2>

Este trabalho constitui a nota da avaliação A3 da UC Sistemas Distribuídos e Mobile.
O trabalho deverá ser feito em equipe com no A3mínimo 3 e no máximo 6
componentes.

<h2> <b>Requisitos</b> </h2>

O trabalho consiste em criar um aplicativo cliente-servidor para reserva de mesas em um restaurante.

O aplicativo deve funcionar da seguinte maneira:

    • Há 3 tipos diferentes de clientes: o atendente de reservas, o garçom e o gerente do restaurante.

    ◦ O atendente de reservas cadastra reservar solicitadas por possíveis frequentadores do restaurante

    ◦ O garçom confirma a ocupação da mesa reservada ao atender um frequentador que fez a reserva

    ◦ O gerente que emite relatórios em tempo real sobre o andamento das reservas

    •Cada tipo de cliente deve ter capturar informações do usuário por meio de um front-end simples (pode ser texto, web, ...)

    • Um servidor hospeda o banco de dados e a parte back-end da aplicação e responde as requisições enviadas pelos clien(atendente, garçom ou gerente).

    • Os dados devem ser armazenados em um banco de dados relacional (ex.MySQL, SQLite, etc.)

    • A aplicação pode ser desenvolvida utilizando as linguagens Python, Java,Javascript, C ou C++

<h2> <b>Detalhamento do Funcionamento da Aplicação</b> </h2>

<h3><b>Cliente Atendente</b> </h3>
    Envia mensagens ao servidor para criar uma reserva ou cancelar uma reserva.
    Uma reserva deve conter data, hora, número da mesa, quantidade de pessoas e nome do responsável (pessoa que encomendou a reserva).
    Ao criar ou cancelar uma reserva o servidor deve retornar uma mensagem informando se a operação foi bem sucedida ou se algum problema ocorreu (ex.: a mesa solicitada já está reservada).
<h3> <b>Cliente Garçom </b> </h3>
    Envia mensagens ao servidor para confirmar que uma reserva feita anteriormente foi utilizada.
    A confirmação do garçom muda o status da mesa. Uma mesa que está reservada, ao ser confirmada, fica novamente livre para receber uma nova reserva em uma data futura.
    Ao confirmar uma reserva o servidor deve retornar uma mensagem informando se a operação foi bem sucedida ou se algum problema ocorreu (ex.: a mesa confirmada não estava reservada).
<h3> <b>Cliente Gerente </b> </h3>
    Envia mensagens ao servidor para solicitar relatórios de acompanhamento das reservas.

    Os relatórios devem ser:

        • Relação de reservas atendidas ou não em um certo período.
        • Relação de reservas feitas para determinada mesa
        • Relação de mesas confirmadas por garçom.
    Ao solicitar um relatório o gerente recebe os dados do relatório ou uma mensagem informando que não há dados que atendem o relatório solicitado.

<h3> <b>Servidor da Aplicação </b> </h3>

    Aguarda mensagens com solicitações de clientes e retorna respostas adequadas.
    Ao receber uma solicitação de cliente, pesquisa e/ou altera as informações no banco de dados e retorna mensagens com respostas ou informações pertinentes ao funcionamento da aplicação.
<h3> <b>Clientes e servidores devem se comunicar usando uma das abordagens demonstradas nas aulas práticas da UC (ex.: Sockets, API, RPC, ...)</b> </h3>
