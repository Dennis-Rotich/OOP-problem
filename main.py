from Judge import Judge

def score_board(arr):
    for contestant in arr:
        judge = Judge(contestant.get('name'),contestant.get('chickenwings'),contestant.get('hamburgers'),contestant.get('hotdogs'))
        judge.save()
    print(Judge.score_points() )   
    Judge.reset()






