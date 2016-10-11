
#include <vector>
#include <iostream>

class Neuron {};

typedef std::vector<Neuron> Layer;

class NeuralBrewery
{
public:
	NeuralBrewery(const std::vector<unsigned> &topology);
	//~NeuralBrewery();
	void feedForward(const std::vector<double> &input) {};
	void backprop(const std::vector<double> &zeta) {};
	void getOutput(std::vector<double> output) const {}; //Perhaps unnecessary function?


private:
	std::vector<Layer> m_layers;

};

	NeuralBrewery::NeuralBrewery(const std::vector<unsigned> &topology)
	{
		unsigned numLayers = topology.size();
		for (unsigned layerNum = 0; layerNum < numLayers; ++layerNum){
			m_layers.push_back(Layer());
			for (int neuronNum = 0; neuronNum <= topology[layerNum]; ++neuronNum)
			{
				m_layers.back().push_back(Neuron());
				/* code */
				std::cout << "Created a new neuron" << std::endl;
			}
		}
	};

int main()
{
	std::vector<unsigned> topology;
	topology.push_back(3);
	topology.push_back(2);
	topology.push_back(1);

	NeuralBrewery Bryggans(topology);

	std::vector<double> input;
	Bryggans.feedForward(input);

	std::vector<double> zeta;
	Bryggans.backprop(zeta);

	std::vector<double> output;
	Bryggans.getOutput(output);


	return 0;
}
