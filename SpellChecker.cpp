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

char* SpellCheckCpp(char* typo, Voctrie* voctrie, Substitutions* substitutions)
{
    std::unordered_map<std::string, double> submap;
    for(int i = 0; i < substitutions->N; i++)
    {
            submap.insert(std::make_pair(std::string(substitutions->spell[i]), substitutions->p[i]));
    }

    double Mp[22][22];
    double maxp = 0;
    char* output = "-ERROR-";
    for(int k = 0; k < voctrie->N; k++)
    {
        char* vocword = voctrie->word[k];
        int i0 = voctrie->prelen[k];
        char spell[22];
        double p = 0;
        for(int i = i0; i < int(strlen(vocword)); i++)
        {
            for(int j = -1; j < int(strlen(typo)); j++)
            {
                strncpy(spell, vocword, i+1);
                spell[i+1] = '>';
                strncpy(spell + i+2, typo, j+1);
                spell[i+j+3] = '\0';
                if(submap.find(std::string(spell)) != submap.end()) p = submap.at(std::string(spell));
                else p = 0;
                for(int n = std::max(i-2, -1); n < i+1; n++)
                {
                    for(int m = std::max(j-2, -1); m < j+1; m++)
                    {
                        if((n!=i)||(m!=j))
                        {
                            strncpy(spell, vocword + n + 1, i-n);
                            spell[i-n] = '>';
                            strncpy(spell + i-n+1, typo + m + 1, j-m);
                            spell[i-n+j-m+1] = '\0';
                            double nextP = 0;
                            if(submap.find(std::string(spell)) != submap.end())
                            {
                                nextP = Mp[n+1][m+1] * submap.at(std::string(spell));
                            }
                            else
                            {
                                nextP = 0;
                            }
                            if(nextP > p)
                            {
                                p = nextP;
                            }
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