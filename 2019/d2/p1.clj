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

(prn (run 0 
  (vec 
    (map 
      #(Integer/parseInt %) 
      (clojure.string/split (slurp "input2") #",")))))

; too low 337024