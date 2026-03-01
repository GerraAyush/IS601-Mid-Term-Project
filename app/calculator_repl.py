# Python Modules
import sys

# App Imports
from app.operation import OperationFactory
from app.calculator import Calculator

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
    calculator = Calculator()

    print("Welcome! I will help with Math. Dumbo.")
    print_operations()

    while True:
        user_operation = input("\nEnter the operation you want to perform: ").strip()

        match user_operation:
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
                print("Not implemented")

            case "load":
                print("Not implemented")

            case "exit":
                print("\nGoodBye! Exiting ...\n")
                sys.exit()

            case _:
                if OperationFactory.is_registered(user_operation):
                    operation = OperationFactory.create_operation(user_operation)
                    calculator.set_operation(operation)

                    operands = []
                    while len(operands) != 2:
                        try:
                            user_input = input(f"Enter operand#{len(operands) + 1}: ").strip()
                            operands.append(float(user_input) if '.' in user_input else int(user_input))
                        except Exception:
                            raise ValueError(f"Invalid operand value: {user_input}")

                    result = calculator.perform_operation(*operands)
                    print(f"Result: {result}")

                else:
                    print(f"Invalid operation: {user_operation}")