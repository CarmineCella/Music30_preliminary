// inclusione delle librerie necessarie
#include "WavFile.h"
#include <iostream>
#include <stdexcept>

// uso del namespace standard
using namespace std;

int main (int argc, char* argv[]) {
    try {
        // controllo degli argomenti
        if (argc != 6) {
            throw runtime_error ("syntax is 'conv input.wav response.wav output.wav scale direct'");
        }

        // apertura dei file argv[0]... argv[n]
        WavInFile x_file (argv[1]);
        WavInFile h_file (argv[2]);
        WavOutFile y_file (argv[3], x_file.getSampleRate (), 16, 1);

        double scale = atof (argv[4]);
        double direct = atof (argv[5]);

        // controllo dei parametri dei file usati
        if (x_file.getSampleRate () != h_file.getSampleRate ()
            || x_file.getNumChannels() != 1 || h_file.getNumChannels() != 1) {
            throw runtime_error ("invalid files provided");
        }

        // allocazione della memoria necessaria (x, h, y)
        int T = x_file.getNumSamples();
        int M = h_file.getNumSamples();
        double* x = new double[T];
        double* h = new double[M];
        double* y = new double[T + M];

        // lettura dei dati da file
        x_file.read (x, T);
        h_file.read (h, M);

        cout << "computing...";
        // convoluzione (due cicli nidificati)
        for (int t = 0; t < T; ++t) {
            for (int m = 0; m < M; ++m) {
                y[t+m] = y[t+m] + x[t] * h[m] * scale; // segnale in convoluz.
            }
            y[t] = y[t] + x[t] * direct; // segnale diretto
        }
        cout << "done" << endl;

        // scrittura del buffer y sul file y_file
        y_file.write (y, T+M);

        // deallocazione dei buffer
        delete [] x;
        delete [] h;
        delete [] y;
    } catch (exception& e) {
        cout << "error: " << e.what () << endl;
    }

    return 0;
}
