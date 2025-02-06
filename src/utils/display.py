from typing import List
from colorama import init, Fore, Style
from ..models.result import Result

# Initialize colorama
init()


def display_results(results: List[Result]):
    print(f"\n{Style.BRIGHT}{
          Fore.CYAN}=== Detailed Test Results ==={Style.RESET_ALL}")

    for i, result in enumerate(results, 1):
        # Create a border around each test
        print(f"\n{Fore.YELLOW}{'═' * 80}{Style.RESET_ALL}")
        print(f"{Style.BRIGHT}{Fore.BLUE}Test #{i}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'─' * 80}{Style.RESET_ALL}")

        # Display prompt with better formatting
        print(f"{Style.BRIGHT}Prompt:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{result.prompt}{Style.RESET_ALL}")

        # Display should_pass status with color
        pass_status = (f"{Fore.GREEN}Yes{Style.RESET_ALL}"
                       if result.should_pass
                       else f"{Fore.RED}No{Style.RESET_ALL}")
        print(f"\n{Style.BRIGHT}Should Pass:{Style.RESET_ALL} {pass_status}")

        # Display LLM response with better formatting
        print(f"\n{Style.BRIGHT}LLM Response:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{result.llm_response}{Style.RESET_ALL}")

    # Add a final border
    print(f"\n{Fore.YELLOW}{'═' * 80}{Style.RESET_ALL}\n")
