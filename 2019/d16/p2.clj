(defn step [num]
  (loop [old (reverse num)
         new (list)
         total 0]
    (if (empty? old)
      new
      (recur (rest old) 
             (conj new (mod (+ total (first old)) 10))
             (+ total (first old))))))

(defn repeat-step [start n]
  (let [target (Integer/parseInt (subs start 0 7))
        num (map #(Integer/parseInt %) (clojure.string/split (subs start target) #""))]
    (last (take (+ n 1) (iterate (fn [x] (step x)) num)))))

(as-> (slurp "input") $
  (apply str (repeat 10000 $))
  (repeat-step $ 100)
  (prn (take 8 $)))
