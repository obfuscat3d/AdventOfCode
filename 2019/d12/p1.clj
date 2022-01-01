(defn make-orb [x y z] {:p [x y z] :v [0 0 0] })
(defn energy [o] (+ (reduce + (o :p) (reduce + (o :v)))))
(defn nep [a] (if (= a 0) 0 (if (< a 0) -1 1)))
(defn energy-sum [orbs] (apply + (map energy orbs)))
(defn energy [o] 
  (* (reduce + (map #(Math/abs %) (o :v))) (reduce + (map #(Math/abs %) (o :p)))))

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

(as-> (slurp "input") $
  (re-seq #"-?\d+" $)
  (map #(Integer/parseInt %) $)
  (partition 3 $)
  (map #(apply make-orb %) $)
  (last (take 1001 (iterate step $)))
  (energy-sum $)
  (println $))
