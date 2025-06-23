from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)
from core.email_api import create_temp_email
from core.credentials import generate_secure_password, generate_name
from web.trimble import create_trimble_account

console = Console()

def main():
    titulo = "[bold blue]Gerador de Contas Trimble[/bold blue]\n"
    subtitulo = "[italic white]Use o período gratuito de teste do SketchUp por 7 dias[/italic white]"
    console.print(Panel(Align.center(titulo + subtitulo), style="cyan", border_style="blue"))

    with console.status("[bold yellow]Preparando ambiente...[/bold yellow]") as status:
        email_data = create_temp_email()
        console.log(f"[green]✅ E-mail temporário criado:[/green] {email_data['email']}")
        
        name = generate_name()
        password = generate_secure_password()
        console.log("[green]✅ Nome e senha seguros gerados.[/green]")

    console.print(Rule(style="blue"))

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console,
            transient=False,
        ) as progress:

            email, pwd = create_trimble_account(
                email=email_data["email"],
                full_name=name,
                password=password,
                email_token=email_data["token"],
                headless=False,
                progress=progress
            )

        console.print(Rule(style="green", title="[bold]Finalizado[/bold]"))
        
        success_panel = Panel.fit(
            f"[bold green]🎉 Conta criada com sucesso![/bold green]\n\n"
            f"📧 [bold cyan]Email:[/bold cyan] {email}\n"
            f"🔑 [bold cyan]Senha:[/bold cyan] {pwd}\n\n"
            "[italic]Agora você pode usar sua conta e iniciar o teste gratuito por 7 dias![/italic]",
            title="[bold magenta]Informações da Conta[/bold magenta]",
            border_style="magenta",
            padding=(1, 2)
        )
        console.print(success_panel)

    except Exception as e:
        console.print(Rule(style="bold red"))
        console.print(f"[bold red]❌ Ocorreu um erro durante a criação da conta:[/bold red]")
        console.print_exception(show_locals=False)


if __name__ == "__main__":
    main()