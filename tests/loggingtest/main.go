package main

import (
	"encoding/json"
	"net/http"

	"go.uber.org/zap"
)

type Payload struct {
	Message    string `json:"message"`
	StatusCode int    `json:"status_code"`
	LogLevel   string `json:"log_level"`
}

func main() {
	logger, _ := zap.NewProduction()
	defer logger.Sync()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var payload Payload
		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
			http.Error(w, "Bad request", http.StatusBadRequest)
			return
		}

		switch payload.LogLevel {
		case "debug":
			logger.Debug(payload.Message)
		case "info":
			logger.Info(payload.Message)
		case "warn":
			logger.Warn(payload.Message)
		case "error":
			logger.Error(payload.Message)
		case "panic":
			logger.Panic(payload.Message)
		case "fatal":
			logger.Fatal(payload.Message)
		default:
			logger.Info(payload.Message)
		}

		w.WriteHeader(payload.StatusCode)
		w.Write([]byte(payload.Message))
	})
	logger.Info("Starting server on port 8080")
	http.ListenAndServe(":8080", nil)
}
