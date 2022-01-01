(def WIDTH 25)
(def HEIGHT 6)

(defn merge-down [l1 l2]
  (apply str (map #(if (= (get l1 %) \2) (get l2 %) (get l1 %)) (range (* HEIGHT WIDTH)))))

(defn flatten-img [layers]
  (reduce #(merge-down %1 %2) (first layers) (rest layers)))

(defn print-image [img]
  (doseq [line (map #(apply str %) (partition-all WIDTH img))]
    (prn line)))

(as-> "input" $
  (slurp $)
  (map #(apply str %) (partition-all (* HEIGHT WIDTH) $))
  (flatten-img $)
  (print-image $))

