package se.kth.jabeja.annealing;

public abstract class NonLinearAnnealer extends Annealer {

    protected float temperature;
    protected float delta;

    NonLinearAnnealer(float initialTemperature, float delta, float alpha) {
        super(initialTemperature, delta, alpha);
        this.temperature = initialTemperature > 0.001 ? initialTemperature : 0.001f;
        this.delta = delta;
    }

    @Override
    public void coolDown() {
        temperature *= delta;
    }
}
