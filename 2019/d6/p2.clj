(defn adj-map-add [adj-map edge]
  (if (contains? adj-map (first edge))
    (conj adj-map {(first edge) (conj (adj-map (first edge)) (second edge))})
    (conj adj-map {(first edge) (list (second edge))})))

(defn create-graph [edges] 
  (loop [edges edges
        adj-map {}]
      (if (= 0 (count edges))
        adj-map
        (recur (rest edges) (as-> adj-map $
                                (adj-map-add $ (first edges))
                                (adj-map-add $ (reverse (first edges)))
                                )))))

(defn get-edges [fn]
  (as-> fn $
    (slurp $)
    (clojure.string/split $ #"\n")
    (map #(clojure.string/split % #"\)") $)))

(defn path-length 
    ([adj-map start end] (path-length adj-map start end #{}))
    ([adj-map start end visited]
      (if (= start end) 
        0
        (as-> (adj-map start) $
          (filter #(not (contains? visited %)) $)
          (map #(path-length adj-map % end (conj visited start)) $)
          (map #(+ 1 %) $)
          (if (= 0 (count $)) 10000 (apply min $))))))

; The way the problem is defined we need to exclude the first
; and final jumps.
(defn part2 [adj-map start end] 
  (- (path-length adj-map start end) 2))

(prn (part2 (create-graph (get-edges "input")) "YOU" "SAN"))
