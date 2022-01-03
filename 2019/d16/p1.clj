(defn mmul [a b] (for [x a] (reduce + (map * x b))))
(defn mod-last-digit [n] (map #(mod (Math/abs %) 10) n))
(defn phase [p n] ([0 1 0 -1] (mod (quot (inc n) p) 4)))

(defn phase-matrix [size]
  (for [i (range 1 (+ 1 size))]
    (for [j (range size)]
      (phase i j))))

(defn repeat-mul [start n]
  (let [mat (phase-matrix (count start))]
    (last (take (+ n 1) (iterate (fn [x] (mod-last-digit (mmul mat x))) start)))))

(as-> (slurp "input") $
  (clojure.string/split $ #"")
  (map #(Integer/parseInt %) $)
  (repeat-mul $ 100)
  (prn (take 8 $)))
