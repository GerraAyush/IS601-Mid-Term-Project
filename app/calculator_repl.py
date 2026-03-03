# Python Modules
import sys
from pathlib import Path

# App Imports
from app.operation import OperationFactory
from app.calculator import Calculator
from app.exceptions import ValidationError, OperationError

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
        project_root = Path(__file__).parent.parent
        history_dir = project_root / "history"
        history_file = history_dir / "calculator_history.csv"
        calculator = Calculator(history_dir=history_dir, history_file=history_file)

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
                continue
            except EOFError:
                print("\nInput terminated. Exiting...")
                break
    
    except Exception as e:
        print(f"Fatal error: {e}")
        raise