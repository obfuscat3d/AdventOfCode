(defn make-orb [x y z] {:p [x y z] :v [0 0 0] })
(defn energy [o] (+ (reduce + (o :p) (reduce + (o :v)))))
(defn nep [a] (if (= a 0) 0 (if (< a 0) -1 1)))

(defn hash-axis [orbs n] 
  (vec (apply concat (mapv #(vec [((% :v) n) ((% :p) n)]) orbs))))

(defn delta-v [pos orbs]
  (as-> (map :p orbs) $
    (map #(map - % pos) $)
    (map #(map nep %) $)
    (apply map + $)))

(defn update-vel [orbs]
  (for [o orbs]
    (into o {:v (mapv + (o :v) (delta-v (o :p) orbs))})))

(defn update-pos [orbs]
  (for [o orbs]
    (into o {:p (mapv + (o :p) (o :v))})))

(defn step [orbs] (update-pos (update-vel orbs)))

(defn axes-frequencies [orbs]
  (loop [orbs orbs
         seen [#{} #{} #{}]]
    (let [h0 (hash-axis orbs 0)
          h1 (hash-axis orbs 1)
          h2 (hash-axis orbs 2)]
      (if (and (contains? (seen 0) h0) (contains? (seen 1) h1) (contains? (seen 2) h2))
        [(count (seen 0)) (count (seen 1)) (count (seen 2))]
        (recur (step orbs) [(conj (seen 0) h0) (conj (seen 1) h1) (conj (seen 2) h2)] )))))

(defn gcd [a b] (if (zero? b) a (gcd b (mod a b))))
(defn lcm [a b] (/ (* a b) (gcd a b)))

(as-> (slurp "input") $
  (re-seq #"-?\d+" $)
  (map #(Integer/parseInt %) $)
  (partition 3 $)
  (map #(apply make-orb %) $)
  (axes-frequencies $)
  (reduce #(lcm %1 %2) $)
  (println $))
