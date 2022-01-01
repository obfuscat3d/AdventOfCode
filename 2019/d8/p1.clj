(def WIDTH 25)
(def HEIGHT 6)

(prn
  (as-> "input" $
    (slurp $)
    (map #(apply str %) (partition-all (* WIDTH HEIGHT) $))
    (map frequencies $)
    (reduce #(if (< (get %1 \0 0) (get %2 \0 0)) %1 %2) {\0 10000} $) 
    (* (get $ \1 0) (get $ \2 0))))
