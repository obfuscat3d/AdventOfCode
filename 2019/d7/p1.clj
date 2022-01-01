;; state = [mem pc input-input]
;; buiffer is a list of ints
(defn make-state [mem pc input output] {:mem mem :pc pc :input input :output output})
(defn nth-digit [x n] (mod (int (/ x (Math/pow 10 n))) 10))
(defn op-code [y] (mod y 100))
(defn param [state n]
  (let [mem (:mem state)
        pc (:pc state)
        ins (get mem pc)]
    (if (= (mod (int (/ ins (* 10 (Math/pow 10 n)))) 10) 1)
      (get mem (+ n pc))
      (get mem (get mem (+ n pc))))))

(defn add [state]
  (let [mem (:mem state)
        pc (:pc state)]
    (make-state (assoc mem (get mem (+ pc 3)) (+ (param state 1) (param state 2))) 
                (+ pc 4)
                (:input state)
                (:output state))))

(defn mul [state]
  (let [mem (:mem state)
        pc (:pc state)]
    (make-state (assoc mem (get mem (+ pc 3)) (* (param state 1) (param state 2))) 
                (+ pc 4)
                (:input state)
                (:output state))))

(defn inp [state]
  (let [mem (:mem state)
        pc (:pc state)]
    (make-state (assoc mem (get mem (+ pc 1)) (first (:input state)))
                (+ 2 pc) 
                (rest (:input state))
                (:output state))))

(defn otp [state]
  (let [mem (:mem state)
        pc (:pc state)]
    ; (prn (param state 1))
    (make-state mem 
                (+ 2 pc) 
                (:input state) 
                (conj (:output state) (param state 1)) )))

(defn jmp-true [state]
  (let [mem (:mem state)
        pc (:pc state)]
    (if (not= 0 (param state 1)) 
      (make-state mem (param state 2) (:input state) (:output state))
      (make-state mem (+ 3 pc) (:input state) (:output state)))))

(defn jmp-false [state]
  (let [mem (:mem state)
        pc (:pc state)]
    (if (= 0 (param state 1)) 
      (make-state mem (param state 2) (:input state) (:output state))
      (make-state mem (+ 3 pc) (:input state) (:output state)))))

(defn lt [state]
  (let [mem (:mem state)
        pc (:pc state)
        a (param state 1)
        b (param state 2)]
    (make-state (assoc mem (get mem (+ pc 3)) (if (< a b) 1 0)) 
                (+ pc 4) 
                (:input state)
                (:output state))))

(defn eq [state]
  (let [mem (:mem state)
        pc (:pc state)
        a (param state 1)
        b (param state 2)]
    (make-state (assoc mem (get mem (+ pc 3)) (if (= a b) 1 0)) 
                (+ pc 4) 
                (:input state)
                (:output state))))

(defn step [state]
  (let [mem (:mem state)
        pc (:pc state)
        op (op-code (get mem pc))]
    (case op
      1 (add state)
      2 (mul state)
      3 (inp state)
      4 (otp state)
      5 (jmp-true state)
      6 (jmp-false state)
      7 (lt state)
      8 (eq state)
      99 (make-state mem -1 (:input state) (:output state)) ; Halt
      :else (throw (Exception. "invalid op code")))))

(defn run 
  [mem input]
    (loop [state (make-state mem 0 input [])] ; empty vec for output
      (if (= (:pc state) -1) ; we've halted
        state
        (recur (step state)))))

(defn load-program [fn] 
  (vec (map #(Integer/parseInt %) (clojure.string/split (slurp fn) #","))))

(defn pp [x] (prn x) x)

(defn valid-phase-seq [x]
  (= 354 (reduce + (map #(int (Math/pow % 4)) (map #(nth-digit x %) (range 5))))))

(defn thruster-signal [phase-seq]
  (let [program (load-program "input")]
    (as->
      (run program (list (nth-digit phase-seq 4) 0)) $
      (run program (list (nth-digit phase-seq 3) (first (:output $))))
      (run program (list (nth-digit phase-seq 2) (first (:output $))))
      (run program (list (nth-digit phase-seq 1) (first (:output $))))
      (run program (list (nth-digit phase-seq 0) (first (:output $)))))))

(defn max-thrust []
  (as-> 
    (range 1234 43211) $
    (filter valid-phase-seq $)
    (pp $)
    (map #(thruster-signal %) $)
    (map #(first (:output %)) $)
    (apply max $)))

(prn (max-thrust))