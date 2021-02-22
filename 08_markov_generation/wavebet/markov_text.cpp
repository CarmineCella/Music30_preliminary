#include <iostream>
#include <deque>
#include <string>
#include <vector>
#include <map>
#include <fstream>

using namespace std;

typedef deque<string> Prefix;
map<Prefix, vector<string> > statetab;

const int NPREF = 3;
const char NONWORD[] = "\n";
const int MAXGEN = 200; // maximum words generated

// add: add word to suffix deque, update prefix void add(Prefix& prefix, const string& s)
void add(Prefix& prefix, const string& s) {
	if (prefix.size() == NPREF) { 
		statetab[prefix].push_back(s);
		prefix.pop_front();
	}
	prefix.push_back(s);
}

// build: read input words, build state table void build(Prefix& prefix, istream& in)
void build (Prefix& prefix, istream& in) {
	string buf;
	while (in >> buf) add (prefix, buf);
}

// generate: produce output, one word per line void generate(int nwords)
void generate(int nwords, ostream& out) {
	Prefix prefix; int i;
	for (i = 0; i < NPREF; i++) add(prefix, NONWORD);
	for (i = 0; i < nwords; i++) {
		vector<string>& suf = statetab[prefix]; 
		const string& w = suf[rand() % suf.size()]; 
		if (w == NONWORD) break;
		out << w << " ";
		if (i % 20 == 0) out << endl;
		prefix.pop_front();
		prefix.push_back(w);
	}
}

int main (void) {
	srand (unsigned (time (NULL)));
	
	int nwords = MAXGEN;
	Prefix prefix; // current input prefix
	for (int i = 0; i < NPREF; i++) {
		add (prefix, NONWORD);
	}
	build (prefix, cin); 
	add (prefix, NONWORD);
	generate (nwords, cout);

	ofstream dictionary ("dict.txt");
	for (map<Prefix, vector<string> >::iterator it = statetab.begin();
		it != statetab.end (); ++it) {
		for (unsigned i = 0; i < it->first.size (); ++i) {
			dictionary << it->first[i] << " ";
		}
		dictionary << "= ";
		for (unsigned i = 0; i < it->second.size (); ++i) {
			dictionary << it->second[i] << " ";
 		}
 		dictionary << endl;
	}
	return 0;
}

// eof