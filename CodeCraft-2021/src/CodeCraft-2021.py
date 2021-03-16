import copy
import sys

server_dict = dict()  # 服务器
vm_dict = dict()  # 虚拟机
op_add_dict = dict()  # 添加操作
op_del_dict = dict()  # 删除操作

op_start_server = dict()  # 虚拟机编号=（服务器编号，虚拟机名称，服务器名称，节点，是否双节点）
day_op_start_server = dict()  # 当天的部署虚拟机操作

max_server_CPU = list()  # CPU最大的服务器
one_max_server_CPU=list()

max_server_RAM = list()  # RAM最大的服务器
one_max_server_RAM=list()

server_id = -1

one_day_dela_id = -1  # 前一天增加的天数编号
one_dela_id = -1  # 前一天的服务器编号
one_new_dela_id = -1

two_day_dela_id = -1  # 前一天增加的天数编号
two_dela_id = -1  # 前一天的服务器编号
two_new_dela_id = -1

maney = 0  # 花费的钱

dep_vm_dict = dict()  # 注册的虚拟机
dela_server_dict = dict()  # 当天购买的服务器
day_dela_server_dict = dict()  # 以往的扩容的服务器

del_op_dict = dict()  # 保存删除的服务器天数与编号
del_op_dict[0] = dict()
del_op_dict[1] = dict()

def main():
    # to read standard input
    # process
    # to write standard output
    # sys.stdout.flush()
    # start = time.time()
    opfile()
    sys.stdout.flush()

    # end = time.time()
    # print(f'结束时间：{end - start}')
    # print(dep_server_dict)
    # print()
    pass


def opfile():
    global server_dict
    global vm_dict
    global op_add_dict
    global op_del_dict
    global max_server_CPU
    global one_max_server_CPU
    global max_server_RAM
    global one_max_server_RAM
    global day_op_start_server  # 每天的操作集
    global day_dela_server_dict  # 当天扩容的服务器
    global dela_server_dict  # 购买的服务器

    global op_start_server  # 当天的操作集

    global one_day_dela_id
    global one_dela_id
    global one_new_dela_id

    global two_day_dela_id
    global two_dela_id
    global two_new_dela_id

    global maney

    # file = open('txt.txt')
    # file = open('training-2.txt')
    # N = file.readline()  # 代表多少台服务器
    N = input()
    sys.stdout.flush()

    # 服务器的配置
    for i in range(int(N)):
        # server = file.readline().split(',')
        server = input().split(',')
        sys.stdout.flush()
        # CPU     内存     成本      能耗成本
        server_list = dict()
        server_list[server[0].strip('(').split()[0]] = [int(server[1].split()[0]), int(server[2].split()[0]), \
                                                        server[3].split()[0], server[4].strip(')\n').split()[0]]
        server_dict[i] = server_list
    max_server_CPU = max_CPU_List(server_dict)
    one_max_server_CPU= [max_server_CPU[0],[max_server_CPU[1][0]//2-1,max_server_CPU[1][1]//2-1,max_server_CPU[1][2],
                                            max_server_CPU[1][3],max_server_CPU[1][0]//2-1,max_server_CPU[1][1]//2-1]]

    max_server_RAM = max_RAM_List(server_dict)
    one_max_server_RAM= [max_server_RAM[0],[max_server_RAM[1][0]//2-1,max_server_RAM[1][1]//2-1,max_server_RAM[1][2],
                                            max_server_RAM[1][3],max_server_RAM[1][0]//2-1,max_server_RAM[1][1]//2-1]]

    # M = file.readline()  # 代表虚拟机的配置
    M = input()
    sys.stdout.flush()
    # 虚拟机
    for i in range(int(M)):
        # vm = file.readline().split(',')
        vm = input().split(',')
        sys.stdout.flush()
        vm_list = [vm[1].split()[0], int(vm[2].split()[0]), int(vm[3].strip(')\n').split()[0])]
        vm_dict[vm[0].strip('(').split()[0]] = vm_list
    # print(vm_dict)

    # T=5
    # s=int(file.readline())  # 天数
    # T = int(file.readline())  # 天数
    T = input()
    sys.stdout.flush()
    # 操作天数
    for i in range(int(T)):
        # R = file.readline()  # 操作数
        R = input()
        sys.stdout.flush()

        dela_server_dict.clear()  # 每天开始时清空上一次循环购买的服务器
        op_start_server.clear()  # 每天开始时清空上一次循环的操作数据
        # 每天操作数
        for r in range(int(R)):
            # op = file.readline().split(',')
            op = input().split(',')
            sys.stdout.flush()
            if len(op) == 2:  # 删除del操作
                op_del_list = [op[0].strip('(').split()[0], op[1].strip(')\n').split()[0]]
                op_del_dict[r] = op_del_list
                op_del(op_del_dict, r, i)
            else:  # 添加add操作
                op_add_list = [op[0].strip('(').split()[0], op[1].split()[0], op[2].strip(')\n').split()[0]]
                op_add_dict[r] = op_add_list
                op_add(op_add_dict, r, i)
        # 一天的操作结束
        # 判断以往天数是否是否为-1，单节点
        if one_day_dela_id == -1:
            one_day_dela_id = i  # 赋值当天的天数
            one_dela_id = copy.deepcopy(one_new_dela_id)  # 复制当天分配的服务器编号
            one_new_dela_id = -1  # 将当天分配的服务器编号设置为-1
        # 双节点
        if two_day_dela_id == -1:
            two_day_dela_id = i  # 赋值当天的天数
            two_dela_id = copy.deepcopy(two_new_dela_id)  # 复制当天分配的服务器编号
            two_new_dela_id = -1  # 将当天分配的服务器编号设置为-1
        day_dela_server_dict[i] = copy.deepcopy(dela_server_dict)  # 深拷贝，保存每天购买的服务器
        day_op_start_server[i] = copy.deepcopy(op_start_server)  # 以天数为键，对当天操作数据保存
        # maney += server_id * int(max_server_CPU[2][3])

    out_str(T)


# 服务器列表，虚拟机列表，操作数列表，当前天数，操作数
def op_add(op_add_dict, op, T):
    CPU = int(vm_dict[op_add_dict[op][1]][0])
    RAM = int(vm_dict[op_add_dict[op][1]][1])
    if vm_dict[op_add_dict[op][1]][2] == 0:  # 单节点部署
        dep_server_vm_one(op_add_dict, op, CPU, RAM, T)
    else:  # 双节点部署
        dep_server_vm_two(op_add_dict, op, CPU, RAM, T)


def dep_server_vm_one(op_dict, op, CPU, RAM, T):
    if len(del_op_dict[0].keys()) != 0:
        for day_id in del_op_dict[0].keys():
            if day_id == T:
                for keys in del_op_dict[0][day_id].keys():
                    server_CPU = int(day_dela_server_dict[day_id][keys][1][0])
                    server_RAM = int(day_dela_server_dict[day_id][keys][1][1])
                    server_CPU_B = int(day_dela_server_dict[day_id][keys][1][4])
                    server_RAM_B = int(day_dela_server_dict[day_id][keys][1][5])
                    if server_CPU>CPU  and server_RAM > RAM:
                        dep_CPU_ARM_key_old(op_dict, op, 'A', keys, 0, CPU, RAM)
                        return
                    if server_CPU_B>CPU  and server_RAM_B > RAM:
                        dep_CPU_ARM_key_old(op_dict, op, 'B', keys, 0, CPU, RAM)
                        return
            else:
                for keys in del_op_dict[0][day_id].keys():
                    server_CPU = int(day_dela_server_dict[day_id][keys][1][0])
                    server_RAM = int(day_dela_server_dict[day_id][keys][1][1])
                    server_CPU_B = int(day_dela_server_dict[day_id][keys][1][4])
                    server_RAM_B = int(day_dela_server_dict[day_id][keys][1][5])
                    if server_CPU>CPU  and server_RAM > RAM:
                        dep_CPU_day_key(op_dict, op, 'A', day_id, keys, 0, CPU, RAM)
                        return
                    if server_CPU_B>CPU  and server_RAM_B > RAM:
                        dep_CPU_day_key(op_dict, op, 'B', day_id, keys, 0, CPU, RAM)
                        return
    if one_new_dela_id != -1:
        server_CPU = int(dela_server_dict[one_new_dela_id][1][0])
        server_RAM = int(dela_server_dict[one_new_dela_id][1][1])

        server_CPU_B = int(dela_server_dict[one_new_dela_id][1][4])
        server_RAM_B = int(dela_server_dict[one_new_dela_id][1][5])
        if server_CPU>CPU  and server_RAM > RAM:
            dep_CPU_ARM_key_old(op_dict, op, 'A', one_new_dela_id, 0, CPU, RAM)
            return
        if server_CPU_B>CPU  and server_RAM_B > RAM:#购买服务器时，重置count=1以便能使用一次b
            dep_CPU_ARM_key_old(op_dict, op, 'B', one_new_dela_id, 0, CPU, RAM)
            return
    elif one_day_dela_id != -1:
        server_CPU = int(day_dela_server_dict[one_day_dela_id][one_dela_id][1][0])
        server_RAM = int(day_dela_server_dict[one_day_dela_id][one_dela_id][1][1])
        server_CPU_B = int(day_dela_server_dict[one_day_dela_id][one_dela_id][1][4])
        server_RAM_B = int(day_dela_server_dict[one_day_dela_id][one_dela_id][1][5])
        if server_CPU>CPU  and server_RAM > RAM:
            dep_CPU_day_key(op_dict, op, 'A', one_day_dela_id, one_dela_id, 0, CPU, RAM)
            return
        if  server_CPU_B> CPU  and server_RAM_B > RAM:
            dep_CPU_day_key(op_dict, op, 'B', one_day_dela_id,one_dela_id, 0, CPU, RAM)
            return
    if CPU>RAM:
        dep_CPU_key(op_dict, op, 'A', 0, CPU, RAM,one_max_server_CPU,'CPU')
    else:
        dep_CPU_key(op_dict, op, 'A', 0, CPU, RAM,one_max_server_RAM,'RAM')


def dep_server_vm_two(op_dict, op, CPU, RAM, T):
    if len(del_op_dict[1].keys()) != 0:
        for day_id in del_op_dict[1].keys():
            if day_id == T:
                for keys in del_op_dict[1][day_id].keys():
                    server_CPU = int(dela_server_dict[keys][1][0])
                    server_RAM = int(dela_server_dict[keys][1][1])
                    if server_CPU - CPU > 0 and server_RAM - RAM > 0:
                        dep_CPU_ARM_key_old(op_dict, op, 'AB', keys, vm_dict[op_dict[op][1]][2], CPU, RAM)
                        return
            else:
                for keys in del_op_dict[1][day_id].keys():
                    server_CPU = int(day_dela_server_dict[day_id][keys][1][0])
                    server_RAM = int(day_dela_server_dict[day_id][keys][1][1])
                    if server_CPU - CPU > 0 and server_RAM - RAM > 0:
                        dep_CPU_day_key(op_dict, op, 'AB', day_id, keys, vm_dict[op_dict[op][1]][2], CPU, RAM)
                        return
    if two_new_dela_id != -1:  # 当天的服务器编号不等于-1
        server_CPU = int(dela_server_dict[two_new_dela_id][1][0])
        server_RAM = int(dela_server_dict[two_new_dela_id][1][1])
        if server_CPU - CPU > 1 and server_RAM - RAM > 1:
            dep_CPU_ARM_key_old(op_dict, op, 'AB', two_new_dela_id, vm_dict[op_dict[op][1]][2], CPU, RAM)
            return
    elif two_day_dela_id != -1:
        server_CPU = int(day_dela_server_dict[two_day_dela_id][two_dela_id][1][0])
        server_RAM = int(day_dela_server_dict[two_day_dela_id][two_dela_id][1][1])
        if server_CPU - CPU > 1 and server_RAM - RAM > 1:
            dep_CPU_day_key(op_dict, op, 'AB', two_day_dela_id, two_dela_id, vm_dict[op_dict[op][1]][2], CPU, RAM)
            return
    if CPU>RAM:
        dep_CPU_key(op_dict, op, 'AB', 1, CPU, RAM,max_server_CPU,'CPU')
    else:
        dep_CPU_key(op_dict, op, 'AB', 1, CPU, RAM,max_server_RAM,'RAM')


# def dep_CPU(op_dict, op, type, day_keys, old_server_id, one_two, CPU, RAM):
#     if day_keys == '' and old_server_id == '':  # 请求新服务器
#         dep_CPU_key(op_dict, op, type, one_two, CPU, RAM)
#     elif day_keys == '' and old_server_id != '':  # 请求当天的服务器
#         dep_CPU_ARM_key_old(op_dict, op, type, old_server_id, one_two, CPU, RAM)
#     else:  # 请求以往的服务器
#         dep_CPU_day_key(op_dict, op, type, day_keys, old_server_id, one_two, CPU, RAM)


# key为空做判断，需要购买服务器
def dep_CPU_key(op_dict, op, type, one_two, CPU, RAM,MAX_CPU_RAM,MAX):
    global dela_server_dict  # 分配的服务器
    global dep_vm_dict  # 分配的虚拟机的服务器所剩余的内存，cpu
    global op_start_server
    global server_id
    global one_new_dela_id  # 单节点当天的服务器id
    global one_day_dela_id  # 当节点前一天的服务器id

    global two_new_dela_id  # 双节点当天的服务器id
    global two_day_dela_id  # 双节点前一天的服务器id

    server_id += 1
    if one_two == 0:  # 单节点
        dela_server_dict [server_id] = copy.deepcopy(one_max_server_RAM)
        one_new_dela_id = copy.deepcopy(server_id)  # 保存服务器编号
        one_day_dela_id = -1  # 使前一天保存的服务器设置为-1判断
    else:  # 双节点
        dela_server_dict [server_id] = copy.deepcopy(max_server_RAM)
        two_new_dela_id = copy.deepcopy(server_id)  # 保存服务器编号
        two_day_dela_id = -1  # 使前一天保存的服务器设置为-1判断

    dela_server_dict[server_id][1][0] -= CPU  # 分配的服务器CPU减去请求的CPU
    dela_server_dict[server_id][1][1] -= RAM  # 分配的服务器内存减去请求的内存

    dep_vm_dict[op_dict[op][2]] = [server_id, op_dict[op][1]]  # 虚拟机id对应部署的服务器,与虚拟机
    # 服务器编号，虚拟机编号，服务器名称，部署节点，是否双节点部署

    op_start_server[op_dict[op][2]] = [server_id, op_dict[op][1], dela_server_dict[server_id][0],type, one_two]


# 操作指令，操作编号，操作节点，是否双节点部署，请求cpu大小，请求内存大小
def dep_CPU_ARM_key_old(op_dict, op, type, old_server_id, one_two, CPU, RAM):
    global dela_server_dict  # 当天分配的服务器
    global dep_vm_dict  # 分配的虚拟机的服务器所剩余的内存，cpu
    global op_start_server  # 当天的操作

    if type=='B':
        dela_server_dict[old_server_id][1][4] -= CPU  # 分配的服务器CPU减去请求的CPU
        dela_server_dict[old_server_id][1][5] -= RAM  # 分配的服务器内存减去请求的内存
    else:
        dela_server_dict[old_server_id][1][0] -= CPU  # 分配的服务器CPU减去请求的CPU
        dela_server_dict[old_server_id][1][1] -= RAM  # 分配的服务器内存减去请求的内存
    dep_vm_dict[op_dict[op][2]] = [old_server_id, op_dict[op][1]]  # 虚拟机id对应部署的服务器,与虚拟机
    # 虚拟机编号=分配的服务器编号，虚拟机名称，当天分配的服务器名称，部署节点，是否双节点部署

    op_start_server[op_dict[op][2]] = [old_server_id, op_dict[op][1], dela_server_dict[old_server_id][0], type,one_two]


# 操作指令，操作编号， 前一天的天数，前一天部署的服务器编号，是否双节点部署，请求的cpu大小，请求的内存大小
def dep_CPU_day_key(op_dict, op, type, day_keys, old_server_id, one_two, CPU, RAM):
    global day_dela_server_dict  # 以往的所以服务器
    global dep_vm_dict  # 分配的虚拟机的服务器所剩余的内存，cpu
    global op_start_server
    if type=='B':
        day_dela_server_dict[day_keys][old_server_id][1][4] -= CPU  # 分配的服务器CPU减去请求的CPU
        day_dela_server_dict[day_keys][old_server_id][1][5] -= RAM  # 分配的服务器内存减去请求的内存
    else:
        day_dela_server_dict[day_keys][old_server_id][1][0] -= CPU  # 分配的服务器CPU减去请求的CPU
        day_dela_server_dict[day_keys][old_server_id][1][1] -= RAM  # 分配的服务器内存减去请求的内存
    dep_vm_dict[op_dict[op][2]] = [old_server_id, op_dict[op][1]]  # 虚拟机id对应部署的服务器,与虚拟机
    # 虚拟机编号=服务器编号，虚拟机名称，服务器名称，部署节点，是否双节点部署
    op_start_server[op_dict[op][2]] = [copy.deepcopy(old_server_id), op_dict[op][1], day_dela_server_dict[day_keys][
        old_server_id][0], type,one_two]

# 操作指令，操作编号，操作天数
def op_del(op_dict, op, d):
    global dela_server_dict
    global day_dela_server_dict
    global op_start_server
    global day_op_start_server
    global del_op_dict
    id = op_dict[op][1]
    if id in op_start_server.keys():  # 当天的添加操作中
        server_id = op_start_server[id][0]
        one_two =op_start_server[id][4]
        if server_id in dela_server_dict.keys():
            CPU = vm_dict[day_op_start_server[server_id][1]][0]
            RAM = vm_dict[day_op_start_server[server_id][1]][1]
            if day_op_start_server[server_id][4] == 1:
                dela_server_dict[server_id][1][0] += CPU
                dela_server_dict[server_id][1][1] += RAM
            else:
                if day_op_start_server[server_id][3] == 'A':
                    dela_server_dict[server_id][2][0] += CPU
                    dela_server_dict[server_id][2][1] += RAM
                else:
                    dela_server_dict[server_id][2][4] += CPU
                    dela_server_dict[server_id][2][5] += RAM
            if d not in del_op_dict[one_two].keys():
                del_op_dict[one_two][d] = dict()
            del_op_dict[one_two][d][server_id] = copy.deepcopy(server_id)
            return
            # op_start_server.pop(vm_id)
    else:
        for day_keys in day_op_start_server.keys():  # 以前添加操作中
            if id in day_op_start_server[day_keys].keys():  # 是否存在改操作中
                server_id = day_op_start_server[day_keys][id][0]
                one_two = day_op_start_server[day_keys][id][4]
                for server_keys in day_dela_server_dict.keys():  # 以往的服务器中
                    CPU = int(vm_dict[day_op_start_server[day_keys][id][1]][0])
                    RAM = int(vm_dict[day_op_start_server[day_keys][id][1]][1])
                    if server_id in day_dela_server_dict[server_keys].keys():
                        if day_op_start_server[day_keys][id][4] == 1:
                            day_dela_server_dict[server_keys][server_id][1][0] += CPU
                            day_dela_server_dict[server_keys][server_id][1][1] += RAM
                        else:
                            if day_op_start_server[day_keys][id][3] == 'A':
                                day_dela_server_dict[server_keys][server_id][1][0] += CPU
                                day_dela_server_dict[server_keys][server_id][1][1] += RAM
                            else:
                                day_dela_server_dict[server_keys][server_id][1][4] += CPU
                                day_dela_server_dict[server_keys][server_id][1][5] += RAM
                        if d not in del_op_dict[one_two].keys():
                            del_op_dict[one_two][server_keys] = dict()
                        del_op_dict[one_two][server_keys][server_id] = copy.deepcopy(server_id)
                        return
                # day_op_start_server[day_keys].pop(id)

# CPU大于RAM
def max_CPU_List(server_dict):
    server_CPU_dict = dict()
    for i in server_dict.keys():
        for j in server_dict[i].keys():
            if server_dict[i][j][0] - server_dict[i][j][1] < 150 and server_dict[i][j][0] - server_dict[i][j][1] > 50:
                server_CPU_dict[j] = server_dict[i][j]
    return max_CPU(server_CPU_dict)

def max_CPU(server_CPU_dict):
    keys = list()
    max_id = ''
    for i in server_CPU_dict.keys():
        keys.append(i)
        for j in server_CPU_dict.keys():
            if j not in keys:
                if server_CPU_dict[i][0] > server_CPU_dict[j][0]:
                    max_id = i
                if server_CPU_dict[i][0] < server_CPU_dict[j][0]:
                    max_id = j
    return [max_id, server_CPU_dict[max_id]]

# CPU大于RAM
def max_RAM_List(server_dict):
    server_RAM_dict = dict()
    for i in server_dict.keys():
        for j in server_dict[i].keys():
            if server_dict[i][j][1] - server_dict[i][j][0] < 150 and server_dict[i][j][1] - server_dict[i][j][0] > 50:
                server_RAM_dict[j] = server_dict[i][j]
    return max_RAM(server_RAM_dict)

def max_RAM(max_RAM_List):
    keys = list()
    max_id = ''
    for i in max_RAM_List.keys():
        keys.append(i)
        for j in max_RAM_List.keys():
            if j not in keys:
                if max_RAM_List[i][0] > max_RAM_List[j][0]:
                    max_id = i
                if max_RAM_List[i][0] < max_RAM_List[j][0]:
                    max_id = j
    return [max_id, max_RAM_List[max_id]]

def out_str(T):
    for i in range(int(T)):
        count_type=dict()
        for j in day_dela_server_dict[i].keys():
            if day_dela_server_dict[i][j][0] not in count_type.keys():
                count_type[day_dela_server_dict[i][j][0]]=1
            else:
                count_type[day_dela_server_dict[i][j][0]]+=1
        print(f'(purchase, {len(count_type.keys())})')
        for key in count_type.keys():
            print(f'({key}, {count_type[key]})')
        print('(migration, 0)')
        sys.stdout.flush()
        for keys in day_op_start_server[i].keys():
            if day_op_start_server[i][keys][4] == 1:
                print(f'({day_op_start_server[i][keys][0]})')
            else:
                print(f'({day_op_start_server[i][keys][0]}, {day_op_start_server[i][keys][3]})')
            # print(day_op_start_server[i][keys])
            sys.stdout.flush()
    # print(maney)


if __name__ == "__main__":
    main()
