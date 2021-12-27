(defn fuel [m] (- (int (/ m 3)) 2))

(prn
  (->> "input"
  slurp
  clojure.string/split-lines
  (map #(Integer/parseInt %))
  (map #(fuel %))
  (reduce +)))
