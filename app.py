
from initUI import run

if __name__ == "__main__":
    try:
        run();
    except Exception as e:
        print(f"except:{e}")
    finally:
        print("final print")
    # return;


