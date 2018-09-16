/*
//  main.cpp
//  hangout-bot
//
//  Copyright © 2018 Carlos Tse <carlos@aboutmy.info>
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

#include <cstdio>
#include <cstdlib>
#include  <sstream>
#include <yaml-cpp/yaml.h>
#include <tgbot/tgbot.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        std::cout << "./hangout-bot [env]" << std::endl;
        exit(1);
    }

    std::string path = "./config/" + std::string(argv[1]) + ".yaml";
    std::cout << "loading config from " << path << std::endl;

    YAML::Node config = YAML::LoadFile(path);
    auto token = config["token"].as<std::string>();

    TgBot::Bot bot(token);

    bot.getEvents().onCommand("start", [&bot](TgBot::Message::Ptr message) {
        bot.getApi().sendMessage(message->chat->id, "Hi!");
    });

    bot.getEvents().onAnyMessage([&bot](TgBot::Message::Ptr message) {
        std::cout << "user wrote " << message->text.c_str() << "\n";
        if (StringTools::startsWith(message->text, "/start")) {
            return;
        }
        bot.getApi().sendMessage(message->chat->id, "Your message is: " + message->text);
    });

    try {
        std::cout << "Bot username: %s" << bot.getApi().getMe()->username.c_str() << std::endl;
        TgBot::TgLongPoll longPoll(bot);
        while (true) {
            std::cout << "Long poll started" << std::endl;
            longPoll.start();
        }
    }
    catch (TgBot::TgException& e) {
        std::cout << "error: " << e.what() << std::endl;
    }
    return 0;
}