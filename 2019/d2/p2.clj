(defn step [pc mem]
  (case (get mem pc)
    1 [(+ pc 4) ; Addition instruction
      (assoc 
        mem 
        (get mem (+ pc 3)) 
        (+ 
          (get mem (get mem (+ pc 1))) 
          (get mem (get mem (+ pc 2)))
        )
      )]
    2 [(+ pc 4)  ; Multiplication instruction
      (assoc 
        mem 
        (get mem (+ pc 3)) 
        (* 
          (get mem (get mem (+ pc 1))) 
          (get mem (get mem (+ pc 2)))
        )
      )]
    99 [-1 mem] ; Halt
    :else (throw (Exception. "invalid op code"))))

;; TODO: loop/recur? I don't think this produces tail recursion
(defn run [pc mem]
  (if 
    (= pc -1) 
    mem 
    (apply run (step pc mem))))

(def mem 
  (vec 
    (map 
      #(Integer/parseInt %) 
      (clojure.string/split (slurp "input2") #","))))

(doseq [i (range 99) j (range 99)]
  (when (= (get (run 0 (assoc (assoc mem 2 j) 1 i)) 0) 19690720)
    (prn i j)))