#include "spherical_harmonics.hpp"

using namespace fsph;
int main(int argc, char **argv)
{
    fsph::PointSPHEvaluator<float> harm(4);

    harm.compute(1, 1);

    for(fsph::PointSPHEvaluator<float>::iterator iter(harm.begin(true)); iter != harm.end(); ++iter)
        std::cout << *iter << ' ';

    std::cout << std::endl;

    const unsigned int sphSize((sphCount(4) + sphCount(3))*3);
    std::cout << sphSize << std::endl;
    std::complex<float> *sphs(new std::complex<float>[sphSize]);

    float phis[] = {0.25, 1.0, 0.5};
    float thetas[] = {0.2, 1.0, 0.85};

    fsph::evaluate_SPH(sphs, 4, phis, thetas, 3, true);

    for(unsigned int i(0); i < sphSize; ++i)
        std::cout << sphs[i] << ' ';

    return 0;
}
