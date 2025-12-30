package main

import (
    "fmt"
    "net/http"
    "log/slog"
    "os"
)

func main() {
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
    
    mux := http.NewServeMux()
    mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello from {{ project_name }} (Go)")
    })

    logger.Info("Starting server on :8080")
    if err := http.ListenAndServe(":8080", mux); err != nil {
        logger.Error("Server failed", "error", err)
        os.Exit(1)
    }
}
