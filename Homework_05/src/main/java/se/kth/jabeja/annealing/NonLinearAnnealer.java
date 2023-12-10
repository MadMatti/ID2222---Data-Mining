package se.kth.jabeja.annealing;

public abstract class NonLinearAnnealer extends Annealer{

    NonLinearAnnealer(float temperature, float delta, float alpha) {
        super(temperature, delta, alpha);
        this.temperature = temperature > 0.001 ? temperature : 0.001;
    }

    @Override
    public void coolDown() {
        temperature *= delta;
    }
}