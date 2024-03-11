#!/bin/zsh
# requires installing virtual enviroment
# Function to handle the 'update' command
update_command() {
    echo "Executing git pull command..."
    git pull
}

# Function to handle the 'run' command
run_command() {
    echo "Running python app.py..."
    python3 app.py
}

# Main script
case "$1" in
    "update")
        update_command
        ;;
    "run")
        run_command
        ;;
    "help")
        echo "Usage: $0 [update | run | help]"
        echo "   update: Perform git pull command"
        echo "   run: Run python app.py"
        ;;
    *)
        echo "Invalid command. Use 'help' command for usage information."
        ;;
esac
