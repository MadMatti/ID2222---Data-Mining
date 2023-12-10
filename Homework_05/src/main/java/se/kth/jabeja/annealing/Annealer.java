package se.kth.jabeja.annealing;

import se.kth.jabeja.Node;

import java.util.*;
import static java.lang.Math.pow;

public abstract class Annealer {

    protected float currentTemperature;
    protected float temperatureDelta;
    protected float alpha;
    protected final Random randomGenerator = new Random();

    Annealer(float initialTemperature, float temperatureDelta, float alpha) {
        this.currentTemperature = initialTemperature;
        this.temperatureDelta = temperatureDelta;
        this.alpha = alpha;
    }

    public void setTemperature(float temperature) {
        this.currentTemperature = temperature;
    }

    public void coolDown() {
        if (currentTemperature > 1) {
            currentTemperature -= temperatureDelta;
        } else {
            currentTemperature = 1;
        }
    }

    protected abstract Double acceptanceProbability(
            Double oldCost, Double newCost, float currentTemperature);

    public Optional<Node> findPartner(
            Node currentNode,
            Node[] candidates,
            HashMap<Integer, Node> entireGraph
    ) {
        return Arrays.stream(candidates)
                .filter(candidate -> acceptanceProbability(
                        calculateCost(currentNode, currentNode.getColor(), candidate, candidate.getColor(), entireGraph),
                        calculateCost(currentNode, candidate.getColor(), candidate, currentNode.getColor(), entireGraph),
                        currentTemperature
                ) > randomGenerator.nextDouble())
                .max(Comparator.comparingDouble(
                        candidate -> calculateCost(
                                currentNode, candidate.getColor(), candidate, currentNode.getColor(), entireGraph)
                ));
    }

    protected Double calculateCost(
            Node nodeP,
            int nodePColor,
            Node nodeQ,
            int nodeQColor,
            HashMap<Integer, Node> entireGraph
    ) {
        return pow(getDegree(nodeP, nodePColor, entireGraph), alpha)
                + pow(getDegree(nodeQ, nodeQColor, entireGraph), alpha);
    }

    protected int getDegree(Node node, int colorId, HashMap<Integer, Node> entireGraph) {
        return (int) node.getNeighbours()
                .stream()
                .map(entireGraph::get)
                .filter(neighbour -> neighbour.getColor() == colorId)
                .count();
    }
}
