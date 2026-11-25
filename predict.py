import json
import sys
import math

THETAS_FILE = "thetas.json"
MAX_MILEAGE = 1_000_000

def load_thetas(path):
	try:
		with open(path) as file:
			thetas_data = json.load(file)
		return float(thetas_data["theta0"]), float(thetas_data["theta1"])
	except FileNotFoundError:
		return 0.0, 0.0
	except (json.JSONDecodeError, KeyError, ValueError):
		print(f"Warning: {path} is invalid, using theta0 = theta1 = 0", file=sys.stderr)
		return 0.0, 0.0

def ask_mileage():
	raw = input("Enter a mileage (km): ").strip()
	if raw == "":
		raise ValueError("input is empty")
	mileage = float(raw)
	if not math.isfinite(mileage): #cases of nan, inf ...
		raise ValueError("mileage must be a finite number")
	if mileage < 0:
		raise ValueError("mileage cannot be negative")
	if mileage > MAX_MILEAGE:
		raise ValueError(f"mileage cannot exceed {MAX_MILEAGE} km")
	return mileage

def estimate_price(mileage, theta0, theta1):
	return theta0 + theta1 * mileage

def main():
	theta0, theta1 = load_thetas(THETAS_FILE)
	try:
		mileage = ask_mileage()
	except ValueError as e:
		print(f"Error: invalid mileage ({e})")
		sys.exit(1)
	except EOFError:
		print("Error: no input received")
		sys.exit(1)
	price = estimate_price(mileage, theta0, theta1)
	print(f"Estimated price for {mileage:.0f} km: {price:.2f}")

if __name__ == "__main__":
	main()