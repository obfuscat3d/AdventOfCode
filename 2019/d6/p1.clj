(defn adj-map-add [adj-map edge]
  (if (contains? adj-map (first edge))
    (conj adj-map {(first edge) (conj (adj-map (first edge)) (second edge))})
    (conj adj-map {(first edge) (list (second edge))})))

(defn create-tree [edges] 
  (loop [edges edges
        adj-map {}]
      (if (= 0 (count edges))
        adj-map
        (recur (rest edges) (adj-map-add adj-map (first edges))))))

(defn get-edges [fn]
  (as-> fn $
    (slurp $)
    (clojure.string/split $ #"\n")
    (map #(clojure.string/split % #"\)") $)))

(defn count-orbits 
  ([adj-map vertex] (count-orbits adj-map vertex 0))
  ([adj-map vertex depth] 
    (if (contains? adj-map vertex)
      (+ depth 
      (reduce + (map #(count-orbits adj-map % (+ depth 1)) (adj-map vertex))))
      depth)))

(prn (count-orbits (create-tree (get-edges "input")) "COM"))