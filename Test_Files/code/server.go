package main

import "fmt"

func main() {
    fmt.Println("Server starting...")
    ch := make(chan string)
    go worker(ch)
    msg := <-ch
    fmt.Println(msg)
}

func worker(ch chan string) {
    defer close(ch)
    ch <- "worker done"
}
