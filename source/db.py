import psycopg2

class Db():

    def __init__(self, setting):
        self.setting = setting

    def getNext(self, user_id):

        connect = psycopg2.connect(self.setting.database_url)
        cursor = connect.cursor()

        cursor.execute("SELECT item_id FROM playbook_bot.current_item where user_id = " + str(user_id))

        if cursor.rowcount == 0:
            res = 1
            cursor.execute("insert into playbook_bot.current_item(user_id, item_id) values({}, 1)".format(user_id))
        else:
            res = cursor.fetchall()[0][0]

            if res == 47:
                res = 1
            else:
                res = res + 1

            cursor.execute("update playbook_bot.current_item set item_id = {} where user_id = {}".format(res, user_id))

        connect.commit()
        connect.close()

        return res

    def getPrev(self, user_id):

        connect = psycopg2.connect(self.setting.database_url)
        cursor = connect.cursor()

        cursor.execute("SELECT item_id FROM playbook_bot.current_item where user_id = " + str(user_id))

        if cursor.rowcount == 0:
            res = 1
            cursor.execute("insert into playbook_bot.current_item(user_id, item_id) values({}, 1)".format(user_id))
        else:
            res = cursor.fetchall()[0][0]
            if res == 1:
                res = 47
            else:
                res = res - 1

            cursor.execute("update playbook_bot.current_item set item_id = {} where user_id = {}".format(res, user_id))

        connect.commit()
        connect.close()

        return res
