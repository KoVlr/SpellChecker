#include <cstring>
#include "unordered_map"

struct Voctrie
{
    char** word;
    int* prelen; //длина слова в родительском узле
    double* p; //вероятность использования слова
    int N; //количество слов
};

struct Substitutions
{
    char** spell; //замена
    double* p; //вероятность замены
    int N;
};

unsigned int hash(char* spell)
{
    unsigned int res = 0;
    unsigned int coefficient = 1;
    int i = 0;
    char c = spell[i];
    while(c != '\0')
    {
        if(c != '>')
        {
            res += (unsigned)c * coefficient;
            coefficient *= 256;
        }
        else coefficient = 65536;
        i++;
        c = spell[i];
    }
    return res;
}

unsigned int hash(char* s1, int n1, char* s2, int n2)
{
    unsigned int res = 0;
    unsigned int coefficient = 1;
    for(int i = 0; i < n1; i++)
    {
        res += unsigned(s1[i]) * coefficient;
        coefficient *= 256;
    }
    coefficient = 65536;
    for(int i = 0; i < n2; i++)
    {
        res += unsigned(s2[i]) * coefficient;
        coefficient *= 256;
    }
    return res;
}

char* SpellCheckCpp(char* typo, Voctrie* voctrie, Substitutions* substitutions)
{
    std::unordered_map<int, double> submap;
    for(int i = 0; i < substitutions->N; i++)
    {
            submap.insert(std::make_pair(hash(substitutions->spell[i]), substitutions->p[i]));
    }

    double Mp[100][100];
    double maxp = 0;
    char* output = voctrie->word[0];
    int typolen = strlen(typo);
    for(int k = 0; k < voctrie->N; k++)
    {
        char* vocword = voctrie->word[k];
        int i0 = voctrie->prelen[k];
        double p;
        int voclen = strlen(vocword);
        int key;
        for(int i = i0; i < voclen; i++)
        {
            for(int j = -1; j < typolen; j++)
            {
                p = 0;
                if((i<2) && (j<2))
                {
                    key = hash(vocword, i+1, typo, j+1);
                    if(submap.find(key) != submap.end()) p = submap.at(key);
                }
                for(int n = (i-2 > -1)?(i-2):(-1); n < i+1; n++)
                {
                    for(int m = (j-2 > -1)?(j-2):(-1); m < j+1; m++)
                    {
                        if((n!=i)||(m!=j))
                        {
                            double nextP = 0;
                            key = hash(vocword+n+1, i-n, typo+m+1, j-m);
                            if(submap.find(key) != submap.end())
                            {
                                nextP = Mp[n+1][m+1] * submap.at(key);
                            }
                            if(nextP > p) p = nextP;
                        }
                    }
                }
                Mp[i+1][j+1] = p;
            }
        }
        p *= voctrie->p[k];
        if(p > maxp)
        {
            maxp = p;
            output = vocword;
        }
    }
    return output;
}


#ifdef __cplusplus
extern "C" {
#endif

char* SpellCheck(char* typo, Voctrie* voctrie, Substitutions* substitutions)
{
    return SpellCheckCpp(typo, voctrie, substitutions);
}

#ifdef  __cplusplus
}
#endif