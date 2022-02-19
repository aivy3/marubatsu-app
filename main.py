import itertools


def get_answer_dict():
    """
    縦横斜めの並んんだ数の合計値で勝敗を判定するために、合計値が被らないように2の累乗のリストに変換する
    1つの値に複合的な条件を入れる時のやり方
    [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ↓
    [1, 2, 4, 8, 16, 32, 64, 128, 256]
    :return:
    """
    num_list = [2 ** i for i in range(9)]
    answer_dict = {}
    for i in range(3):
        # 横の合計
        _num_list = num_list[i * 3:(i + 1) * 3]
        answer_dict.update({sum(_num_list): _num_list})
        # 縦の合計
        _num_list = [num_list[i + 3 * j] for j in range(3)]
        answer_dict.update({sum(_num_list): _num_list})
    # 斜め
    _num_list = [num_list[4 * i] for i in range(3)]
    answer_dict.update({sum(_num_list): _num_list})
    _num_list = [num_list[2 * (i + 1)] for i in range(3)]
    answer_dict.update({sum(_num_list): _num_list})
    return answer_dict


def check_win(selected_list, answer_list):
    """
    勝敗の判定
    playerが選択した数字のlistから３つを取り出して合計値がanswer_listの中にあれば勝ち
    :param selected_list:
    :param answer_list:
    :return:
    """
    if len(selected_list) >= 3:
        for selected_num in itertools.combinations(selected_list, 3):
            if sum(list(selected_num)) in answer_list:
                return True
        return False
    else:
        return False


def get_com_number_level(com_num_list, player_selected_list, coordinate_list, level):
    """
    レベル別コンピュータの最善手
    :param com_num_list:
    :param player_selected_list:
    :param coordinate_list:
    :param level:
    :return:
    """
    num_list = [2 ** i for i in range(9)]
    answer_dict = get_answer_dict()
    evaluation_dict = {a: 0 for a in answer_dict}
    com_evaluation_dict = {}
    player_evaluation_dict = {}
    for answer_num in evaluation_dict:
        # コンピュータが選択した数字が含まれるかを計算
        # 全ての合計値1379と&を取ることでその数字が入っているか否かを判断できる（以下2つのmatch_listの計算は同じ結果になる）
        # match_list = list(filter(lambda x: 1379 & x == x, com_num_list))
        com_match_list = list(filter(lambda x: answer_num // x % 2 == 1, com_num_list))
        player_match_list = list(filter(lambda x: answer_num // x % 2 == 1, player_selected_list))
        com_evaluation_dict[answer_num] = com_match_list
        player_evaluation_dict[answer_num] = player_match_list

    # 要素が含まれているのが多い順に並び替え
    sorted_com_evaluation = sorted(com_evaluation_dict.items(), key=lambda x: len(x[1]), reverse=True)
    sorted_player_evaluation = sorted(player_evaluation_dict.items(), key=lambda x: len(x[1]), reverse=True)

    if level == '3':
        # 最初に真ん中が取れる場合は最優先
        if int(coordinate_list[4]) > 0:
            cal_num = coordinate_list[4]
            return cal_num
        # 既に2つ以上揃っている箇所があれば残りをとる=勝ち
        for k, val_list in sorted_com_evaluation:
            if len(val_list) == 2:
                selectable_num_list = answer_dict[k]
                for n in selectable_num_list:
                    idx = num_list.index(n)
                    if int(coordinate_list[idx]) > 0:
                        cal_num = coordinate_list[idx]
                        return cal_num

    # 相手が2つ以上揃えている場合は阻止する
    if level in ['2', '3']:
        for k, val_list in sorted_player_evaluation:
            if len(val_list) == 2:
                selectable_num_list = answer_dict[k]
                for n in selectable_num_list:
                    idx = num_list.index(n)
                    if int(coordinate_list[idx]) > 0:
                        cal_num = coordinate_list[idx]
                        return cal_num

    cal_num = None
    # 優先度の高い要素から順番に確認していく
    for k, val_list in sorted_com_evaluation:
        selectable_num_list = answer_dict[k]
        for n in selectable_num_list:
            idx = num_list.index(n)
            # 選択ずみの要素はcoordinate_listの中身が-1に置き換えらているので0より大きいで確認する
            if int(coordinate_list[idx]) > 0:
                cal_num = coordinate_list[idx]
                break
    if not cal_num:
        cal_num = list(filter(lambda x: int(x) > 0, coordinate_list))[0]
    return cal_num


def main():
    answer_dict = get_answer_dict()
    answer_list = [a for a in answer_dict]
    player1_selected_list = []
    player2_selected_list = []
    turn_user = 0
    turn_count = 0
    err_message = '正しい座標を入力してください。'

    print('コンピュータのレベルを選択してください(レベル1〜3)')
    while True:
        level = input('1, 2, 3のいずれかをの数値をいれてください')
        if level not in ['1', '2', '3']:
            print('レベルは1か2か3しか選べません。')
            continue
        else:
            print(f'level_{level}で対戦します。')
            break
    print('以下の数字で座標を指定してください')
    text = """
    1|2|3
    -----
    4|5|6
    -----
    7|8|9
    """
    print(text)
    coordinate_list = [str(i) for i in range(1, 10)]
    candidates = [2 ** i for i in range(9)]

    while True:
        if turn_user == 0:
            player1_input = input('playerの入力')
            if player1_input in coordinate_list:
                text = text.replace(str(player1_input), "o")
                idx = coordinate_list.index(player1_input)
                coordinate_list[idx] = "-1"
                player1_selected_list.append(candidates[idx])
                print(text)
                if check_win(player1_selected_list, answer_list):
                    print('player1の勝ち')
                    break
            else:
                print(err_message)
                continue
            turn_user = 1
            turn_count += 1
        else:
            print('コンピュータが入力')
            player2_input = get_com_number_level(player2_selected_list, player1_selected_list, coordinate_list, level)
            if player2_input in coordinate_list:
                text = text.replace(str(player2_input), "x")
                idx = coordinate_list.index(player2_input)
                coordinate_list[idx] = "-1"
                player2_selected_list.append(candidates[idx])
                print(text)
                if check_win(player2_selected_list, answer_list):
                    print('コンピュータの勝ち')
                    break
            else:
                print(err_message)
                continue
            turn_user = 0
            turn_count += 1
        if turn_count == 9:
            print("引き分けです")
            break


if __name__ == "__main__":
    main()