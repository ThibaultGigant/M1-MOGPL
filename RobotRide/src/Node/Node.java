package Node;

import java.util.List;

/**
 * Created by Tigig on 17/11/2015.
 * Classe qui servira à représenter les croisements de rails avec leurs coordonnées et leur direction
 */
public class Node {
    private Point p;
    private Direction d;
    private List<Node> adjacents;

    public Point getCoordonnees() {
        return p;
    }

    public Direction getDirection() {
        return d;
    }

    public List<Node> getAdjacents() {
        return adjacents;
    }
}
