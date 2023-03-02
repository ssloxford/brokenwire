class IPerfEvaluation():

    noise_level = 0
    lime_sdr_gain = 0
    output_power = 0
    jitter = 0
    lost = 0
    sent = 0
    loss = 100
    
    def __init__(self, distance, amplifier, voltage, current, preamble, evaluation_time, cable_length, angle, antenna_position, antenna):
        self.distance = distance
        self.amplifier = amplifier
        self.voltage = voltage
        self.current = current
        self.preamble = preamble
        self.evaluation_time = evaluation_time
        self.cable_length = cable_length
        self.angle = angle
        self.antenna_position = antenna_position
        self.antenna = antenna
    
    def to_dict(self):
        return self.__dict__
    
    def print(self):
        print(f"IPerf Evaluation:\n\tDistance: {self.distance}\n\tAmplifier: {self.amplifier}\n\tVoltage: {self.voltage}\n\tCurrent: {self.current}\n\tPreamble: {self.preamble}\n\tEvaluation Time: {self.evaluation_time}\n\tCable Length: {self.cable_length}\n\tAngle: {self.angle}\n\tAntenna Position: {self.antenna_position}\n\tAntenna: {self.antenna}")
        
    def print_results(self):
        print(f"Results for Noise Level: {self.noise_level} and Gain: {self.lime_sdr_gain}\nLost: {self.lost}\nSent: {self.sent}\nLoss: {self.loss}")
