package se.kth.jabeja.annealing;

import static java.lang.Math.exp;

public class BoltzmannAnnealer extends NonLinearAnnealer {

    BoltzmannAnnealer(float temperature, float delta, float alpha) {
        super(temperature, delta, alpha);
    }

    @Override
    protected Double acceptanceProbability(Double oldCost, Double newCost, float temperature) {
        return 1 / (1 + exp(-(newCost - oldCost) / temperature));
    }
}
