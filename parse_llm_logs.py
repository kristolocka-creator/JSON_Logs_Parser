import json
import sys
import statistics

TOKEN_THRESHOLD = 1000

def load_logs(path):
    logs = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            record = json.loads(line)
            logs.append(record)

    return logs

def filter_logs(logs):
    filtered = []

    for record in logs:
        if not isinstance(record, dict):
            print("Предупреждение: запись должна быть объектом JSON", file=sys.stderr)
            continue

        if "tokens_used" not in record:
            continue

        if not isinstance(record["tokens_used"], (int, float)):
            print("Предупреждение: tokens_used должен быть числом", file=sys.stderr)
            continue

        if record["tokens_used"] > TOKEN_THRESHOLD:
            filtered.append(record)

    return filtered

def save_logs(logs, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(logs, file, ensure_ascii=False, indent=2)

def save_report(report, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(report, file, ensure_ascii=False, indent=2)

def calculate_total_tokens(logs):
    total = 0

    for record in logs:
        if "tokens_used" not in record:
            continue

        total += record["tokens_used"]

    return total

def calculate_avg_latency(logs):
    latencies = []

    for record in logs:
        if "latency_ms" not in record:
            continue

        if not isinstance(record["latency_ms"], (int, float)):
            print("Предупреждение: latency_ms должен быть числом", file=sys.stderr)
            continue

        latencies.append(record["latency_ms"])

    if not latencies:
        return None

    return sum(latencies) / len(latencies)

def calculate_median_latency(logs):
    latencies = []

    for record in logs:
        if "latency_ms" not in record:
            continue

        if not isinstance(record["latency_ms"], (int, float)):
            print("Предупреждение: latency_ms должен быть числом", file=sys.stderr)
            continue

        latencies.append(record["latency_ms"])

    if not latencies:
        return None

    return statistics.median(latencies)

def main():
    try:
        logs = load_logs("data/empty.json")
        filtered_logs = filter_logs(logs)

        save_logs(filtered_logs, "results/filtered_logs.json")

        total_tokens = calculate_total_tokens(filtered_logs)

        avg_latency = calculate_avg_latency(filtered_logs)

        median_latency = calculate_median_latency(filtered_logs)

        report = {
            "total_entries": len(logs),
            "filtered_entries": len(filtered_logs),
            "token_threshold": TOKEN_THRESHOLD,
            "total_tokens": total_tokens,
            "avg_latency_ms": round(avg_latency, 2) if avg_latency is not None else None,
            "median_latency_ms": median_latency,
        }
        save_report(report, "results/report.json")
        print(f"Всего обработано: {len(logs)}")
        print(f"Отфильтровано: {len(filtered_logs)}")
        print(f"Порог токенов: {TOKEN_THRESHOLD}")
        print(f"Всего токенов: {total_tokens}")
        if avg_latency is not None:
            print(f"Средняя задержка: {avg_latency:.2f} мс")
        else:
            print("Средняя задержка: нет данных")

        if median_latency is not None:
            print(f"Медианная задержка: {median_latency:.2f} мс")
        else:
            print("Медианная задержка: нет данных")

    except FileNotFoundError:
        print("Ошибка: файл не найден: data/logs.json", file=sys.stderr)
        return 1

    except json.JSONDecodeError:
        print("Ошибка: файл содержит невалидный JSON", file=sys.stderr)
        return 1

    return 0

if __name__ == "__main__":
    raise SystemExit(main())