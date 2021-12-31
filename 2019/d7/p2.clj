(defn make-state 
    ([mem pc input output] (make-state mem pc input output false))
    ([mem pc input output paused]
     {:mem mem :pc pc :input input :output output :paused paused }))

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
    ;(prn (param state 1))
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
    (if (= pc -1) (throw (Exception. "tried to start a halted process")))
    (case op
      1 (add state)
      2 (mul state)
      ;; Just return current state when blocking on input
      3 (if (empty? (:input state)) (make-state mem pc () (:output state) true) (inp state))
      4 (otp state)
      5 (jmp-true state)
      6 (jmp-false state)
      7 (lt state)
      8 (eq state)
      99 (make-state mem -1 (:input state) (:output state)) ; Halt
      :else (throw (Exception. "invalid op code")))))

(defn run 
  [mem pc input]
    (loop [state (make-state mem pc input [])] ; empty vec for output
      (if (or (= (:pc state) -1) (:paused state)); we've halted or it's paused
        state
        (recur (step state)))))

(defn load-program [fn] 
  (vec (map #(Integer/parseInt %) (clojure.string/split (slurp fn) #","))))

(defn pp [x] (prn x) x)

(defn valid-phase-seq [x] ; now for all digits 5-9
  (= 14979 (reduce + (map #(int (Math/pow % 4)) (map #(nth-digit x %) (range 5))))))

;; Default to pc=0, amplifier number as input. Output vec doesn't matter.
(defn init-states [program phase-seq]
  {0 (make-state program 0 (list (nth-digit phase-seq 4)) [])
   1 (make-state program 0 (list (nth-digit phase-seq 3)) [])
   2 (make-state program 0 (list (nth-digit phase-seq 2)) [])
   3 (make-state program 0 (list (nth-digit phase-seq 1)) [])
   4 (make-state program 0 (list (nth-digit phase-seq 0)) [])})

(defn thruster-signal [phase-seq]
  (let [program (load-program "input") ]
    (loop [ i 0
            states (init-states program phase-seq)
            first true]
      (let [cur (get states i)
            last (get states (mod (- i 1) 5))
            new-input (:output last) ]
        (if (and (= i 0) (= -1 (:pc last)))
          (:output last)
          (recur (mod (+ 1 i) 5)
                 (conj states 
                       {i (run (:mem cur) 
                               (:pc cur) 
                               ;; Use last input aside from the first input
                               (concat (:input cur) (if first (list 0) new-input)))})
                  false))))))


(defn max-thrust []
  (as-> 
    (range 56789 98766) $
    (filter valid-phase-seq $)
    (map #(thruster-signal %) $)
    (map #(first %) $)
    (apply max $)))

(prn (max-thrust))