// wavebet.cpp
//


#include "WavFile.h"
#include <stdexcept>
#include <iostream>
#include <fstream>
#include <map>
#include <deque>
#include <vector>

using namespace std;

typedef deque<char> Prefix;
typedef map<Prefix, vector<char> > StateTab;

// add: add word to suffix deque, update prefix void add(Prefix& prefix, const string& s)
void add(Prefix& prefix, char s, int npref, StateTab& tab) {
	if (prefix.size() == npref) { 
		tab[prefix].push_back(s);
		prefix.pop_front();
	}
	prefix.push_back(s);
}

// build: read input words, build state table void build(Prefix& prefix, istream& in)
void build (Prefix& prefix, char* data, int len, int npref, StateTab& tab) {
	for (int i = 0; i < len; ++i) {
		add (prefix, data[i], npref, tab);
	}
}

// generate: produce output, one word per line void generate(int nwords)
void generate(Prefix& current, StateTab& tab, int nwords, double memory, char* out) {
	for (int i = 0; i < nwords; i++) {
		char pw = 0;
		vector<char>& suf = tab[current]; 
		if (suf.size () == 0) continue;
		char w = suf[rand() % suf.size()]; 
		
		char f = (char)(memory * (double) pw + (1. - memory) * (double) w);
		pw = w;
		out[i] = f;
		current.pop_front();
		current.push_back(w);
	}
}

// -----
int main (int argc, char* argv[]) {
	srand (unsigned (time (NULL)));

	cout << "[wavebet, ver. 0.1]" << endl << endl;
	cout << "markovian sample-based generation" << endl << endl;

	try {
		if (argc != 5) {
			throw runtime_error ("syntax is 'wavebet learn.wav duration order memory'");
		}

		cout << "reading input\n"; cout.flush();
		WavInFile in (argv[1]);
		if (in.getNumBits () != 16 || in.getNumChannels()!= 1) {
			throw runtime_error ("invalid file format for learning (only 16-bit mono supported)");
		}

		int sr = in.getSampleRate ();
		long samples = in.getNumSamples();

		int gen_samples = (long) (atof (argv[2]) * (double) sr);
		if (gen_samples <= 0) {
			throw runtime_error ("invalid duration specified");
		}

		int order = atol (argv[3]);
		if (order < 1) throw runtime_error ("invalid order specified");

		double memory = atof (argv[4]);
		if (memory < 0 || memory >= 1) throw runtime_error ("invalid memory specified");

		cout << "allocating memory\n"; cout.flush();
		short* buffer = new short[samples];
		char* buffer8 = new char[samples]; // 8-bit vector quantization
		char* buffer8_out = new char[gen_samples]; // 8-bit vector quantization
		short* buffer_out = new short[gen_samples]; 

		cout << "reading input\n"; cout.flush();
		in.read (buffer, samples);
		for (unsigned i = 0; i < samples; ++i) {
			buffer8[i] = (char) ((double) buffer[i] / 32768. * 128);
		}

		StateTab tab;
		Prefix prefix; // current input prefix

		cout << "building transitions "; cout.flush();
		build (prefix, buffer8, samples, order, tab);

		cout << "(size " << tab.size () << ")" << endl; cout.flush ();
		StateTab::iterator p = tab.begin ();
		std::advance (p, (rand () % tab.size()));
		Prefix current = p->first;

		cout << "generating\n"; cout.flush();
		generate (current, tab, gen_samples, memory, buffer8_out);

		cout << "saving output\n"; cout.flush();
		for (unsigned i = 0; i < gen_samples; ++i) {
			buffer_out[i] = (short) ((double) buffer8_out[i] / 128. * 32768.);
		}		
		WavOutFile out("gen.wav", sr, 16, 1);
		out.write (buffer_out, gen_samples);

		cout << "cleaning memory\n"; cout.flush ();
		delete [] buffer;
		delete [] buffer8;
		delete [] buffer_out;
		delete [] buffer8_out;
	}
	catch (exception& e) {
		cout << "Error: " << e.what () << endl;
	}
	catch (...) {
		cout << "Fatal error: unknown exception" << endl;
	}
	return 0;
}

// EOF
