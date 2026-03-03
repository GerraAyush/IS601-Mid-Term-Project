# Python Modules
import sys
import logging

# App Imports
from app.calculator import Calculator
from app.utils import get_project_root
from app.operation import OperationFactory
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError, OperationError
from app.history import LoggingObserver, AutoSaveObserver


def print_operations():
    print("Available commands:")
    print(OperationFactory.list_operations())
    print("  help - Show all available operations")
    print("  history - Show calculation history")
    print("  clear - Clear calculation history")
    print("  undo - Undo the last calculation")
    print("  redo - Redo the last undone calculation")
    print("  save - Save calculation history to file")
    print("  load - Load calculation history from file")
    print("  exit - Exit the calculator")

def calculator_repl():
    try:
        config = CalculatorConfig(base_dir=get_project_root())
        calculator = Calculator(config)
        
        calculator.add_observer(LoggingObserver())
        calculator.add_observer(AutoSaveObserver(calculator))

        print("Welcome! I will help with Math. Dumbo.")
        print_operations()

        while True:
            try:
                command = input("\nEnter the operation you want to perform: ").strip()

                match command:
                    case "help":
                        print_operations()

                    case "history":
                        calculator.show_history()
                    
                    case "clear":
                        calculator.clear_history()
                        print("Cleared history.")

                    case "undo":
                        if calculator.undo():
                            print("Undo successful!")
                        else:
                            print("Nothing to undo")

                    case "redo":
                        if calculator.redo():
                            print("Redo successful!")
                        else:
                            print("Nothing to redo")

                    case "save":
                        try:
                            calculator.save_history()
                            print("History saved successfully")
                        except Exception as e:
                            print(f"Error saving history: {e}")

                    case "load":
                        try:
                            calculator.load_history()
                            print("History loaded successfully")
                        except Exception as e:
                            print(f"Error loading history: {e}")

                    case "exit":
                        print("\nGoodBye! Exiting ...\n")
                        sys.exit()

                    case _:
                        try:
                            operation = OperationFactory.create_operation(command)
                            calculator.set_operation(operation)

                            operands = []
                            while len(operands) != 2:
                                try:
                                    user_input = input(f"Enter operand#{len(operands) + 1}: ").strip()
                                    operands.append(float(user_input) if '.' in user_input else int(user_input))
                                except Exception:
                                    raise OperationError(f"Invalid operand value: {user_input}")

                            result = calculator.perform_operation(*operands)
                            print(f"Result: {result}")

                        except (ValidationError, OperationError) as e:
                            print(f"Error: {e}")

                        except Exception:
                            print(f"Unknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nOperation cancelled")
                logging.info("Operation cancelled")
                continue
            except EOFError:
                print("\nInput terminated. Exiting...")
                logging.info("Input terminated. Exiting...")
                break
    
    except Exception as e:
        print(f"Fatal error: {e}")
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise