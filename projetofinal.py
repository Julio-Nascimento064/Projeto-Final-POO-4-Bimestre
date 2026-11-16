from datetime import datetime


class Pessoa:
    """Classe base para representar pessoas da livraria."""

    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("O nome não pode ficar vazio.")
        self._nome = valor.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise ValueError("E-mail inválido. Informe um endereço com '@' e domínio.")
        self._email = valor.strip()

    def exibir_dados(self) -> str:
        return f"Nome: {self.nome} | E-mail: {self.email}"

    def atualizar_contato(self, novo_email: str):
        self.email = novo_email


class Usuario(Pessoa):
    """Representa um usuário da biblioteca que pode retirar livros."""

    def __init__(self, nome: str, matricula: int, email: str):
        super().__init__(nome, email)
        self.matricula = matricula
        self.emprestimos = []

    @property
    def matricula(self) -> int:
        return self._matricula

    @matricula.setter
    def matricula(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("Matrícula inválida. Use um número inteiro positivo.")
        self._matricula = valor

    def solicitar_emprestimo(self, emprestimo: "Emprestimo") -> "Emprestimo":
        self.emprestimos.append(emprestimo)
        emprestimo.usuario = self
        return emprestimo

    def devolver_livro(self, emprestimo: "Emprestimo", livro: "Livro") -> str:
        if livro in emprestimo.livros:
            emprestimo.livros.remove(livro)
            livro.atualizar_status(True)
            return f"Livro '{livro.titulo}' devolvido com sucesso."
        return f"O livro '{livro.titulo}' não está neste empréstimo."

    def __str__(self) -> str:
        return f"Usuário: {self.nome} | Matrícula: {self.matricula}"


class Funcionario(Pessoa):
    """Representa o colaborador responsável pelo atendimento da livraria."""

    def __init__(self, nome: str, email: str, cargo: str):
        super().__init__(nome, email)
        self.cargo = cargo

    def registrar_emprestimo(self, usuario: Usuario, emprestimo: "Emprestimo") -> str:
        usuario.solicitar_emprestimo(emprestimo)
        return f"Empréstimo {emprestimo.numero_emprestimo} registrado para {usuario.nome}."

    def __str__(self) -> str:
        return f"Funcionário: {self.nome} | Cargo: {self.cargo}"


class Livro:
    """Representa um livro do acervo da livraria."""

    def __init__(self, titulo: str, autor: str, disponivel: bool = True):
        self.titulo = titulo
        self.autor = autor
        self.disponivel = disponivel

    def verificar_disponibilidade(self) -> bool:
        return self.disponivel

    def atualizar_status(self, disponivel: bool):
        self.disponivel = disponivel

    def __str__(self) -> str:
        status = "Disponível" if self.disponivel else "Emprestado"
        return f"{self.titulo} - {self.autor} ({status})"


class Emprestimo:
    """Registra a retirada de um ou mais livros por um usuário."""

    def __init__(self, numero_emprestimo: int, data_retirada: str, usuario: Usuario = None):
        self.numero_emprestimo = numero_emprestimo
        self.data_retirada = data_retirada
        self.usuario = usuario
        self.livros = []

    def adicionar_livro(self, livro: Livro):
        if not livro.verificar_disponibilidade():
            raise ValueError(f"O livro '{livro.titulo}' não está disponível no momento.")
        self.livros.append(livro)
        livro.atualizar_status(False)

    def calcular_multa(self, dias_atraso: int = 0, taxa_diaria: float = 2.5) -> float:
        if taxa_diaria == 0:
            raise ZeroDivisionError("Taxa diária inválida. A taxa não pode ser zero.")
        return dias_atraso * taxa_diaria

    def __str__(self) -> str:
        nomes = ", ".join(livro.titulo for livro in self.livros) if self.livros else "Nenhum livro"
        return (
            f"Empréstimo #{self.numero_emprestimo} | Data: {self.data_retirada} | "
            f"Usuário: {self.usuario.nome if self.usuario else 'Não informado'} | Livros: {nomes}"
        )


def ler_inteiro(mensagem: str, minimo: int = None, maximo: int = None) -> int:
    """Lê um número inteiro com validação contínua."""
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                raise ValueError(f"O valor deve ser maior ou igual a {minimo}.")
            if maximo is not None and valor > maximo:
                raise ValueError(f"O valor deve ser menor ou igual a {maximo}.")
            return valor
        except ValueError:
            print("Entrada inválida. Digite apenas números inteiros.")


def ler_float(mensagem: str, minimo: float = None) -> float:
    """Lê um número decimal com validação contínua."""
    while True:
        try:
            valor = float(input(mensagem))
            if minimo is not None and valor < minimo:
                raise ValueError(f"O valor deve ser maior ou igual a {minimo}.")
            return valor
        except ValueError:
            print("Entrada inválida. Digite apenas números válidos.")


def calcular_media_livros_por_emprestimo(total_livros: int, total_emprestimos: int) -> float:
    """Calcula a média de livros por empréstimo com proteção contra divisão por zero."""
    try:
        if total_emprestimos == 0:
            raise ZeroDivisionError("Não há empréstimos registrados para calcular a média.")
        return total_livros / total_emprestimos
    except ZeroDivisionError:
        raise ZeroDivisionError("Não foi possível calcular a média: não há empréstimos registrados.")


def buscar_livro_por_indice(livros: list[Livro], indice: int) -> Livro:
    try:
        return livros[indice]
    except IndexError:
        raise IndexError("Índice inválido. Esse livro não existe na lista atual.")


def exibir_menu():
    print("\n===== MENU DA LIVRARIA =====")
    print("1 - Exibir dados do funcionário")
    print("2 - Exibir dados do usuário")
    print("3 - Calcular multa estimada")
    print("4 - Ver relatório de média de livros por empréstimo")
    print("5 - Buscar livro por índice")
    print("6 - Sair")


def executar_menu(funcionario: Funcionario, usuario: Usuario, livros: list[Livro], emprestimos: list[Emprestimo]):
    while True:
        exibir_menu()
        try:
            opcao = ler_inteiro("Escolha uma opção: ", minimo=1, maximo=6)

            if opcao == 1:
                print(funcionario.exibir_dados())
            elif opcao == 2:
                print(usuario)
            elif opcao == 3:
                dias = ler_inteiro("Digite os dias de atraso: ", minimo=0)
                taxa = ler_float("Digite a taxa diária (ex.: 2.5): ", minimo=0)
                try:
                    print(f"Multa estimada: R$ {emprestimos[0].calcular_multa(dias, taxa):.2f}")
                except ZeroDivisionError as erro:
                    print(f"Erro de operação: {erro}")
                except IndexError:
                    print("Erro de operação: não existe empréstimo registrado para calcular a multa.")
                except ValueError:
                    print("Erro de operação: valores inválidos para cálculo de multa.")
            elif opcao == 4:
                total_livros = ler_inteiro("Quantidade total de livros: ", minimo=0)
                total_emprestimos = ler_inteiro("Quantidade total de empréstimos: ", minimo=0)
                try:
                    resultado = calcular_media_livros_por_emprestimo(total_livros, total_emprestimos)
                    print(f"Média de livros por empréstimo: {resultado:.2f}")
                except ZeroDivisionError as erro:
                    print(f"Erro de cálculo: {erro}")
            elif opcao == 5:
                if not livros:
                    print("Erro de operação: não há livros cadastrados.")
                    continue
                for indice, livro in enumerate(livros):
                    print(f"[{indice}] {livro}")
                indice = ler_inteiro("Digite o índice do livro: ", minimo=0, maximo=len(livros) - 1)
                try:
                    livro_escolhido = buscar_livro_por_indice(livros, indice)
                    print(f"Livro encontrado: {livro_escolhido}")
                except IndexError as erro:
                    print(f"Erro de busca: {erro}")
            elif opcao == 6:
                print("Saindo do sistema da livraria. Até logo!")
                break

        except ValueError as erro:
            print(f"Entrada inválida: {erro}")


if __name__ == "__main__":
    try:
        funcionario = Funcionario("Ana Souza", "ana@livraria.com", "Bibliotecária")
        usuario = Usuario("João Pedro", 202401, "joao@email.com")

        livro1 = Livro("Dom Casmurro", "Machado de Assis")
        livro2 = Livro("O Pequeno Príncipe", "Antoine de Saint-Exupéry")
        livros = [livro1, livro2]

        emprestimo = Emprestimo(101, datetime.today().strftime("%d/%m/%Y"), usuario)
        usuario.solicitar_emprestimo(emprestimo)
        emprestimos = [emprestimo]

        try:
            emprestimo.adicionar_livro(livro1)
            emprestimo.adicionar_livro(livro2)
        except ValueError as erro:
            print(f"Erro ao registrar livros: {erro}")

        print(funcionario.exibir_dados())
        print(usuario)
        print(emprestimo)
        print(f"Disponibilidade do livro 1: {livro1.verificar_disponibilidade()}")
        print(f"Multa estimada: R$ {emprestimo.calcular_multa(3):.2f}")

        print(usuario.devolver_livro(emprestimo, livro1))
        print(f"Disponibilidade após devolução: {livro1.verificar_disponibilidade()}")

        executar_menu(funcionario, usuario, livros, emprestimos)
    except ValueError as erro:
        print(f"Erro de validação do sistema: {erro}")
    except IndexError as erro:
        print(f"Erro de índice: {erro}")
    except ZeroDivisionError as erro:
        print(f"Erro de operação: {erro}")
