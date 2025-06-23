from rich.console import Console
from rich.console import Group
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
    with console.status("[bold yellow]Preparando ambiente...[/bold yellow]") as status:
        email_data = create_temp_email()
        log_email = f"[green]✅ E-mail temporário criado:[/green] {email_data['email']}"
        
        name = generate_name()
        password = generate_secure_password()
        log_password = "[green]✅ Email e senha gerados.[/green]"

    try:
        progress_output = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=40),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            email, pwd = create_trimble_account(
                email=email_data["email"],
                full_name=name,
                password=password,
                email_token=email_data["token"],
                headless=False,
                progress=progress
            )

        final_rule = Rule(style="green", title="[bold]Finalizado[/bold]")

        success_panel = Panel.fit(
            f"[bold green]🎉 Conta criada com sucesso![/bold green]\n\n"
            f"📧 [bold cyan]Email:[/bold cyan] {email}\n"
            f"🔑 [bold cyan]Senha:[/bold cyan] {pwd}\n\n"
            "[italic]Agora você pode usar sua conta e iniciar o teste gratuito por 7 dias![/italic]",
            title="[bold magenta]Informações da Conta[/bold magenta]",
            border_style="magenta",
            padding=(1, 2)
        )

        output_group = Group(
            log_email,
            log_password,
            final_rule,
            success_panel
        )
        console.print(Panel(output_group, border_style="blue", title="[bold]Criação da Conta[/bold]", padding=(1, 2)))

    except Exception as e:
        error_panel = Panel.fit(
            f"[bold red]❌ Ocorreu um erro durante a criação da conta:[/bold red]\n\n[dim]{str(e)}",
            border_style="red"
        )
        console.print(error_panel)
        console.print_exception(show_locals=False)
    finally:
        input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()